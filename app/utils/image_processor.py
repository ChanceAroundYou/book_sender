from pathlib import Path
import cv2
import numpy as np
import logging
from typing import Tuple
from ..config import settings

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, debug: bool = False):
        """
        Initialize ImageProcessor
        :param debug: If True, save debug images to temporary directory
        """
        self.debug = debug

    def _save_debug_image(self, image: np.ndarray, mark: str, image_path: Path):
        """
        Save debug image to temporary directory
        :param image: The image to save
        :param mark: Image name
        :param image_path: Original image path
        """
        if not self.debug:
            return
            
        debug_dir = settings.TMP_DIR / "debug_images"
        debug_dir.mkdir(exist_ok=True, parents=True)
        debug_path = debug_dir / f"{image_path.stem}_{mark}.png"
        cv2.imwrite(str(debug_path), image)
        logger.debug(f"保存调试图像: {debug_path}")

    def find_checkbox(self, image_path: str | Path) -> Tuple[int, int] | None:
        """
        Find checkbox in the image and return its center coordinates

        :param image_path: Image file path
        :return: If checkbox is found, return its center coordinates (x, y); otherwise return None
        """
        # Read image
        if isinstance(image_path, str):
            image_path = Path(image_path)
        if not image_path.exists():
            logger.error(f"Image file does not exist: {image_path}")
            return None
        
        img = cv2.imread(str(image_path))
        if img is None:
            logger.error(f"Cannot read image: {image_path}")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        self._save_debug_image(binary, "binary", image_path)

        # Find contours
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= 1000]
        if not contours:
            logger.debug("No outer contour found")
            return None
        
        contour = contours[0]
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)

        # Build image with outer contour
        inner_contour_img = img.copy()
        cv2.drawContours(inner_contour_img, [contour], -1, (0, 255, 0), 2)
        self._save_debug_image(inner_contour_img, "contours", image_path)

        # Extract ROI
        roi = binary[y:y+h, x:x+w]
        roi_img = img[y:y+h, x:x+w].copy()

        # Find inner contours in ROI
        inner_contours, _ = cv2.findContours(
            roi, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        inner_contours = [cnt for cnt in inner_contours if area * 0.8 > cv2.contourArea(cnt) > 400]
        if not inner_contours:
            logger.debug("No inner contour found for checkbox")
            return None
        
        inner_contour = inner_contours[0]

        inner_contour_img = roi_img.copy()
        cv2.drawContours(inner_contour_img, inner_contours, -1, (0, 255, 0), 2)
        self._save_debug_image(inner_contour_img, "inner_contours", image_path)

        inner_x, inner_y, inner_w, inner_h = cv2.boundingRect(inner_contour)

        center_x = x + inner_x + inner_w // 2
        center_y = y + inner_y + inner_h // 2

        # Mark the found checkbox on the image
        result_img = img.copy()
        cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(result_img, 
                            (x+inner_x, y+inner_y), 
                            (x+inner_x+inner_w, y+inner_y+inner_h), 
                            (255, 0, 0), 2)
        cv2.circle(result_img, (center_x, center_y), 3, (0, 0, 255), -1)
        self._save_debug_image(result_img, "result", image_path)

        logger.debug(f"Found checkbox at: ({center_x}, {center_y})")
        return center_x, center_y

import cv2
import numpy as np
import logging
import os
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, debug: bool = False):
        """
        初始化图像处理器
        :param debug_mode: 是否保存调试图像
        """
        self.debug = debug
        self.debug_dir = "debug_images"
        if self.debug:
            os.makedirs(self.debug_dir, exist_ok=True)

    def _save_debug_image(self, image: np.ndarray, name: str, image_path: str):
        """
        保存调试图像
        :param image: 要保存的图像
        :param name: 图像名称
        :param image_path: 原始图像路径
        """
        if not self.debug:
            return
            
        # 从原始图像路径中提取文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        # 构建调试图像保存路径
        debug_path = os.path.join(self.debug_dir, f"{base_name}_{name}.png")
        cv2.imwrite(debug_path, image)
        logger.debug(f"保存调试图像: {debug_path}")

    def find_checkbox(self, image_path: str) -> Optional[Tuple[int, int]]:
        """
        在图像中查找 checkbox
        :param image_path: 图像文件路径
        :return: 如果找到 checkbox，返回其中心点坐标 (x, y)；否则返回 None
        """
        # 读取图像
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"无法读取图像: {image_path}")
            return None

        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 使用自适应阈值处理
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        self._save_debug_image(binary, "binary", image_path)
        
        # 查找轮廓
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= 1000]
        if not contours:
            logger.debug("未找到外框")
            return None
        
        contour = contours[0]
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)

        # 创建轮廓可视化图像
        inner_contour_img = img.copy()
        cv2.drawContours(inner_contour_img, [contour], -1, (0, 255, 0), 2)
        self._save_debug_image(inner_contour_img, "contours", image_path)

        # 提取ROI区域
        roi = binary[y:y+h, x:x+w]
        roi_img = img[y:y+h, x:x+w].copy()

        # 在ROI中查找内部轮廓
        inner_contours, _ = cv2.findContours(
            roi, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        inner_contours = [cnt for cnt in inner_contours if area * 0.8 > cv2.contourArea(cnt) > 400]
        if not inner_contours:
            logger.debug("未找到checkbox内框")
            return None
        
        inner_contour = inner_contours[0]

        inner_contour_img = roi_img.copy()
        cv2.drawContours(inner_contour_img, inner_contours, -1, (0, 255, 0), 2)
        self._save_debug_image(inner_contour_img, "inner_contours", image_path)

        inner_x, inner_y, inner_w, inner_h = cv2.boundingRect(inner_contour)

        center_x = x + inner_x + inner_w // 2
        center_y = y + inner_y + inner_h // 2
                        
                # 在图像上标记找到的 checkbox
        result_img = img.copy()
        cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(result_img, 
                            (x+inner_x, y+inner_y), 
                            (x+inner_x+inner_w, y+inner_y+inner_h), 
                            (255, 0, 0), 2)
        cv2.circle(result_img, (center_x, center_y), 3, (0, 0, 255), -1)
        self._save_debug_image(result_img, "result", image_path)
                        
        logger.debug(f"找到 checkbox，位置: ({center_x}, {center_y})")
        return center_x, center_y

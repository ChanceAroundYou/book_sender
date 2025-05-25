import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from loguru import logger
from sqlalchemy.orm import Session

from app.database import Book, User, get_denpend_db

router = APIRouter()


@router.get("/image-proxy")
async def image_proxy(request: Request, url: str = Query(...)):
    """
    Proxies an image from an external URL.
    Helps to avoid CORS issues when displaying images from third-party domains.
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required.")

    # Basic validation for common image extensions, can be expanded
    allowed_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")
    if not any(url.lower().endswith(ext) for ext in allowed_extensions):
        # Allow if no extension but looks like a URL from a known good source (if necessary)
        # For now, stricter check. Could also check Content-Type after fetching.
        # logger.warning(f"Image proxy attempt for URL with potentially non-image extension: {url}")
        # Consider if we want to proceed or raise an error here.
        # For now, we let it try, but a real production system might be stricter.
        pass  # Allowing to proceed, but a more robust solution might check Content-Type header later

    async with httpx.AsyncClient() as client:
        try:
            # Make a GET request to the external URL, following redirects
            # Timeout can be adjusted as needed
            response = await client.get(url, follow_redirects=True, timeout=10.0)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses

            content_type = response.headers.get(
                "content-type", "application/octet-stream"
            )
            if not content_type.startswith("image/"):
                logger.error(
                    f"Proxied URL {url} did not return an image. Content-Type: {content_type}"
                )
                raise HTTPException(
                    status_code=400, detail="The linked resource is not a valid image."
                )

            # Stream the response content back to the client
            return StreamingResponse(response.iter_bytes(), media_type=content_type)

        except httpx.TimeoutException:
            logger.error(f"Timeout when trying to proxy image from {url}")
            raise HTTPException(
                status_code=504, detail="Gateway timeout while fetching image."
            )
        except httpx.RequestError as e:
            logger.error(f"Error proxying image from {url}: {e}")
            # Avoid leaking too much detail about the external error if sensitive
            raise HTTPException(
                status_code=502,
                detail=f"Bad gateway while fetching image: {e.__class__.__name__}",
            )
        except HTTPException as e:  # Re-raise our own HTTPErrors
            raise e
        except Exception as e:
            logger.error(f"Unexpected error proxying image from {url}: {e}")
            raise HTTPException(
                status_code=500, detail="Internal server error while proxying image."
            )


@router.get("/utils/stats/total-books")
async def get_total_books(db: Session = Depends(get_denpend_db)):
    """Get total number of books in database"""
    with db as db:
        total = db.query(Book).count()
        return {"total": total}


@router.get("/utils/stats/total-users")
async def get_total_users(db: Session = Depends(get_denpend_db)):
    """Get total number of users in database"""
    with db as db:
        total = db.query(User).count()
        return {"total": total}

import logging
import time
from fastapi import Request, Response


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)


# @app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")

    try:
        body = await request.json()
        # print("Request Body")
        # print(body)
        logger.debug(f"Request body: {body}")
    except Exception:
        print("ABC")

    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time

    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    # Recreate the response with the original body
    response = Response(content=body, status_code=response.status_code, headers=dict(response.headers))

    logger.info(f"Response: {response.status_code} | Time: {process_time:.2f}s | response: {response.body}")
    return response


import json
import time
import logging

from fastapi import Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)

class CustomResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            response: Response = await call_next(request)  # Process request
            duration = time.time() - start_time

            headers = dict(response.headers)
            headers.pop('content-length', None)

            # Log request details
            log_message = (
                f"{request.client.host}:{request.client.port} - "
                f'"{request.method} {request.url.path} {request.scope["http_version"]}" '
                f"{response.status_code} "
                f"Time Taken: {duration:.4f} seconds"
            )
            logging.info(log_message)

            # If response is streaming (e.g., chatbot), do not modify it
            if isinstance(response, StreamingResponse):
                return response

            # Handle empty 204 (No Content) responses
            if response.status_code == 204:
                return Response(status_code=204)

            # Read response body
            response_body = [section async for section in response.__dict__['body_iterator']]
            original_data = json.loads(response_body[0].decode()) if response_body else None

            # Format response for success (200-299)
            if 200 <= response.status_code < 205:
                response_data = {
                    "succeeded": True,
                    "status_code": response.status_code,
                    "message": self.get_success_message(response.status_code),
                    "data": original_data,
                }
                return JSONResponse(content=response_data, headers=headers, status_code=response.status_code)

            # Return unmodified response for non-2xx status codes
            return response

        except Exception as e:
            logging.error(f"Unhandled exception: {e}", exc_info=True)

            error_response = {
                "succeeded": False,
                "status_code": 500,
                "message": "An unexpected error occurred.",
                "error_details": str(e),
            }

            return JSONResponse(content=error_response, headers=headers, status_code=500)

    @staticmethod
    def get_success_message(status_code):
        """
        Generate a success message based on the status code.
        """
        success_messages = {
            200: "Request processed successfully.",
            201: "Resource created successfully.",
            202: "Request accepted for processing.",
            204: "No content available.",
        }
        return success_messages.get(status_code, "Operation completed successfully.")

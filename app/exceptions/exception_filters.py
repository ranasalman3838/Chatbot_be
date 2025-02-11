from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

async def exception_handler(request, exc):
    """
    Global exception handler for various types of exceptions in FastAPI application.

    Args:
        request: The incoming request
        exc: The exception that was raised

    Returns:
        JSONResponse with structured error information
    """
    error_response = {
        "succeeded": False,
        "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "Internal Server Error",
        "error_details": []
    }

    try:
        match exc:
            case RateLimitExceeded():
                error_response["statusCode"] = status.HTTP_429_TOO_MANY_REQUESTS
                error_response["message"] = "Too Many Requests"
                error_response["error_details"] = "Rate limit exceeded. Please try again later"

            case RequestValidationError():
                error_response["statusCode"] = status.HTTP_422_UNPROCESSABLE_ENTITY
                error_response["message"] = "Validation Error"
                error_details = [
                    {
                        "type": error.get("type", "validation_error"),
                        "field": (error["loc"][1] if len(error.get("loc", [])) > 1 else error["loc"][0])
                        if error.get("loc") else "unknown",
                        "error": (
                            error.get('ctx', {}).get('error') or
                            error.get("msg", "Unknown validation error")
                        )
                    }
                    for error in exc.errors()
                ]
                error_response["error_details"] = error_details

            case StarletteHTTPException():
                error_response["statusCode"] = exc.status_code
                error_response["message"] = str(exc.detail)

                # Special handling for 404 Not Found
                if exc.status_code == status.HTTP_404_NOT_FOUND:
                    error_response["message"] = "Resource not found"
                    error_response["error_details"] = [
                        {
                            "path": str(request.url.path),
                            "method": request.method
                        }
                    ]

            case SQLAlchemyError():
                error_response["statusCode"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_response["message"] = "Database Error"
                error_response["error_details"] = [str(exc)]

                # Log the specific database error for debugging
                logger.error(f"SQLAlchemy Error: {exc}", exc_info=True)

            case ValueError():
                error_response["statusCode"] = status.HTTP_400_BAD_REQUEST
                error_response["message"] = "Value Error"
                error_response["error_details"] = [str(exc)]

            case _:
                # Catch-all for unexpected errors
                error_response["statusCode"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_response["error_details"] = [
                    {
                        "type": type(exc).__name__,
                        "error": str(exc)
                    }
                ]

                logger.error(f"Unexpected error type {type(exc).__name__}: {exc}", exc_info=True)

    except Exception as handling_exc:
        # Handle exceptions raised within the exception handler itself
        logger.error(f"Error in exception handler: {handling_exc}", exc_info=True)
        error_response["message"] = "Error processing the exception"
        error_response["error_details"] = [str(handling_exc)]

    return JSONResponse(
        status_code=error_response["statusCode"],
        content=error_response
    )
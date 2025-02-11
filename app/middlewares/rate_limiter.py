from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


def init_rate_limiting(app: FastAPI):
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

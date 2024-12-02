from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.common.middlewares.logger import LogRequestsMiddleware
from app.common.utils.logger import app_logger
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    if route and route.tags and route.name:
        return f"{route.tags[0]}-{route.name}"
    return ""


app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# app.include_router(api_router, prefix=settings.API_PREFIX)
app.add_middleware(LogRequestsMiddleware, logger=app_logger)


@app.get("/")
def home():
    return {"message": "Welcome to Election App!!"}

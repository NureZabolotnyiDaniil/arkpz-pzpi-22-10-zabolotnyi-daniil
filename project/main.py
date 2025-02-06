from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routers.admin.views import router as admin_router
from routers.lantern.views import router as lantern_router
from routers.renovation.views import router as renovation_router
from routers.breakdown.views import router as breakdown_router
from routers.park.views import router as park_router
from routers.statistics.views import router as statistics_router
from routers.repairman.views import router as repairman_router
from routers.company.views import router as company_router
from iot.views import router as iot_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(openapi_url="/openapi.json", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)
app.include_router(lantern_router)
app.include_router(breakdown_router)
app.include_router(renovation_router)
app.include_router(park_router)
app.include_router(repairman_router)
app.include_router(company_router)
app.include_router(statistics_router)
app.include_router(iot_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SmartLighting API",
        version="1.0",
        description="SmartLighting arkpz project",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path, methods in openapi_schema["paths"].items():
        for method, details in methods.items():
            if not (path.startswith("/admin/") and method == "post"):
                details["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

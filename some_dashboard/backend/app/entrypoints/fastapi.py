from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from entrypoints.view.dashboards import dashboard_router

view_router = APIRouter(
    routes=[
        *dashboard_router.routes,
    ]
)


def raise_exc(request, exc):
    """Raises an exception to bypass built-in Starlette and FastAPI error handlers"""
    raise exc


def create_app():
    app = FastAPI(
        title="Just_pretty_dashboard",
        docs_url="/api/docs",
    )

    app.include_router(view_router)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app

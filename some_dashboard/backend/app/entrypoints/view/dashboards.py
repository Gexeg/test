from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from service.queries.get_sql_query_durations import get_query_durations
from service.queries.get_slowest_queries import get_slowest_queries
from service.queries.get_popular_queries import get_popular_queries

dashboard_router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")


@dashboard_router.get("/", response_class=HTMLResponse)
async def main_view(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@dashboard_router.get("/queries_dashboard", response_class=HTMLResponse)
async def get_query_dashboard(request: Request):
    chart_data = await get_query_durations()
    slowest_queries = await get_slowest_queries()
    return templates.TemplateResponse(
        "queries_dashboard/index.html",
        {
            "request": request,
            "chart_data": chart_data,
            "chart_title": chart_data["title"],
            "table": slowest_queries,
        },
    )


@dashboard_router.get("/slowest_queries", response_class=HTMLResponse)
async def get_slowest(request: Request):
    slowest_queries = await get_slowest_queries()
    return templates.TemplateResponse(
        "queries_dashboard/components/table.html",
        {
            "request": request,
            "table": slowest_queries,
        },
    )


@dashboard_router.get("/popular_queries", response_class=HTMLResponse)
async def get_popular(request: Request):
    slowest_queries = await get_popular_queries()
    return templates.TemplateResponse(
        "queries_dashboard/components/table.html",
        {
            "request": request,
            "table": slowest_queries,
        },
    )


@dashboard_router.get("/sales_dashboard", response_class=HTMLResponse)
async def get_sales_dashboard(request: Request):
    return templates.TemplateResponse(
        "sales_dashboard/index.html",
        {
            "request": request,
        },
    )

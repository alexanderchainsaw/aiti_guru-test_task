from fastapi import APIRouter

from .views.orders.views import router as orders_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(orders_router, prefix="/orders")

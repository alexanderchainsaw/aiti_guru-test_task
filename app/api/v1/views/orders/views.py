from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.repository.exceptions import EntityDoesntExistException
from app.repository.orders.exceptions import (
    NotEnoughProductException,
    ProductOutOfStockException,
)
from app.repository.orders.models import OrderItemRaw
from app.repository.repository_controller import RepositoryControllerTransact

router = APIRouter(
    route_class=DishkaRoute
)


@router.post(
    "/{order_id}/product",
    response_model=OrderItemRaw,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Указаны ID несуществующих сущностей"},
        status.HTTP_409_CONFLICT: {
            "description": "Товара по данному ID нет в наличии"
            " или количество товара в запросе превышает доступное кол-во продукции"
        },
        status.HTTP_201_CREATED: {
            "description": "Товара не было в заказе, товар добавлен в заказ",
        },
        status.HTTP_200_OK: {
            "description": "Товар уже присутствовал в заказе, количество товара в заказе увеличено",
        },
    },
)
async def add_product_to_order(
    repo: FromDishka[RepositoryControllerTransact],
    order_id: int,
    product_id: int = Query(description="ID товара"),
    quantity: int = Query(description="Кол-во товара", gt=0),
):
    try:
        created = await repo.orders.add_product_to_order(
            order_id=order_id, product_id=product_id, quantity=quantity
        )
    except EntityDoesntExistException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указаны ID несуществующих сущностей",
        )
    except ProductOutOfStockException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Товара по данному ID нет в наличии",
        )
    except NotEnoughProductException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Количество в запросе превышает количество доступного товара",
        )
    if created.quantity == quantity:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(created))
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(created))

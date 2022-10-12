from src.endpoints.order import (
    fetchOrdersQuery,
    createOrderQuery,
    updateOrderStatusQuery,
)
from src.endpoints.user_regist import create_user
from tests.helper import delete_user
import pytest
from src.dbconnector import connExecute
from src.schematypes import Product, ProductPayload


def test_fullOrderWorkflow():
    """
    Tests the fetchOrdersQuery function, which queries the database for a user's orders.
    """
    __cleanup_orders()  # cleanup just in case

    # create user
    assert create_user("order_user", "password", "test@email.com")

    # no orders == blank
    assert [] == fetchOrdersQuery("order_user")

    # repeated product ID should raise exception
    with pytest.raises(Exception):
        assert createOrderQuery(
            "order_user",
            [{"product_id": 1, "quantity": 1}, {"product_id": 1, "quantity": 10}],
        )

    # create order
    for _ in range(2):
        assert createOrderQuery(
            "order_user",
            [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 10}],
        )

    # fetch order
    orders = fetchOrdersQuery("order_user")
    assert len(orders) == 2

    # check newly placed order status
    assert orders[0].order_status == "placed"

    # check product ids and quantities are correct
    prodPayloads = list(
        map(
            lambda prodPayload: (prodPayload.product.product_id, prodPayload.quantity),
            orders[1].products,
        )
    )
    assert (1, 1) in prodPayloads and (2, 10) in prodPayloads

    # update order status
    updateOrderStatusQuery(orders[0].order_id, "cancelled")

    # fetch order and check status has been updated
    orders = fetchOrdersQuery("order_user")
    assert len(orders) == 2
    assert (
        next(
            filter(lambda order: order.order_id == orders[0].order_id, orders)
        ).order_status
        == "cancelled"
    )

    __cleanup_orders()


def __cleanup_orders():
    connExecute([(('DELETE from "Orderline"'),)])
    connExecute([(('DELETE from "Order"'),)])
    delete_user("order_user")

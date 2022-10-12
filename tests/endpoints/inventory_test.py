from src.endpoints.order import (
    fetchOrdersQuery,
    createOrderQuery,
    updateOrderStatusQuery,
)
from src.endpoints.user_regist import create_user
from tests.helper import delete_user
import pytest
from src.dbconnector import connExecute
from src.endpoints.inventory import (
    updateInventoryQuery,
    updateProductOffsetQuery,
    getInventoryQuery,
    getProductOffsets,
)


def test_inventoryWorkflow():
    """
    Tests the inventory workflow."""
    __cleanup_inventory()

    # create user
    create_user("inv_user", "password", "test@email.com")
    assert getInventoryQuery("inv_user") == []

    # add inventory
    updateInventoryQuery("inv_user", 1, 10)

    # check inventory
    __checkInventoryForProduct(1, 10)

    # add order
    createOrderQuery(
        "inv_user",
        [{"product_id": 1, "quantity": 1}],
    )
    __checkInventoryForProduct(1, 10)

    # fulfil order and check inv is incremented
    orders = fetchOrdersQuery("inv_user")
    updateOrderStatusQuery(orders[0].order_id, "fulfilled")
    __checkInventoryForProduct(1, 11)

    # check that offset is 9 if we set total inventory to 10, since order for 1 unit was fulfilled
    updateInventoryQuery("inv_user", 1, 10)
    __checkInventoryForProduct(1, 10)

    offsets = getProductOffsets("inv_user")
    selectedProdPayload = next(
        filter(
            lambda prodPayload: prodPayload.product.product_id == 1,
            offsets,
        )
    )
    assert selectedProdPayload.quantity == 9

    # update offset manually back to 10, resulting in an expected inventory total of 11
    updateProductOffsetQuery("inv_user", 1, 10)
    __checkInventoryForProduct(1, 11)

    __cleanup_inventory()


def __checkInventoryForProduct(prod_id, quantity):
    newInv = getInventoryQuery("inv_user")
    selectedProdPayload = next(
        filter(
            lambda prodPayload: prodPayload.product.product_id == prod_id,
            newInv,
        )
    )
    assert selectedProdPayload.quantity == quantity


def __cleanup_inventory():
    connExecute([(('DELETE from "UserProductOffset"'),)])
    connExecute([(('DELETE from "Orderline"'),)])
    connExecute([(('DELETE from "Order"'),)])
    delete_user("inv_user")

from src.schematypes import (
    Supplier,
    Product,
    ProductPayload,
    sumProductPayloads,
)
import pytest


def test_sumProductPayloads():
    """
    Tests the sumProductPayloads function.
    """
    supplier = Supplier(supplier_id=1, name="Test Supplier")

    product1 = Product(product_id=1, name="Test Product 1", supplier=supplier)
    product2 = Product(product_id=2, name="Test Product 2", supplier=supplier)

    payload1 = ProductPayload(product=product1, quantity=1)
    payload2 = ProductPayload(product=product2, quantity=2)
    payload3 = ProductPayload(product=product1, quantity=3)
    payload4 = ProductPayload(product=product2, quantity=4)
    payload5 = ProductPayload(product=product1, quantity=5)
    nonePayload = None

    # summing a None with a ProductPayload should return the ProductPayload
    assert sumProductPayloads(nonePayload, payload1) == payload1

    # summing a ProductPayload with a None should return the ProductPayload
    assert sumProductPayloads(payload2, nonePayload) == payload2

    # summing two ProductPayloads with the same product ID should return a ProductPayload with the sum of the quantities
    assert sumProductPayloads(payload1, payload3) == ProductPayload(
        product=product1, quantity=4
    )

    # should be able to chain sums
    assert sumProductPayloads(
        payload1, sumProductPayloads(payload3, payload5)
    ) == ProductPayload(product=product1, quantity=9)

    # summing two ProductPayloads with different product IDs should raise a ValueError
    with pytest.raises(ValueError):
        sumProductPayloads(payload3, payload4)

    # summing Nones should raise a ValueError
    with pytest.raises(ValueError):
        sumProductPayloads(nonePayload, nonePayload)

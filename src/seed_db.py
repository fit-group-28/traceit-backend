import random
from endpoints.user_regist import create_user
from endpoints.order import createOrderQuery, updateOrderStatusQuery


if __name__ == "__main__":
    username = "testuser1"
    password = "password"

    # create a user
    create_user(username, password, "email@address.com")

    orderIds = []

    for _ in range(40):
        products = [
            {"product_id": j + 1, "quantity": random.randint(1, 100)} for j in range(3)
        ]

        orderIds.append(createOrderQuery(username, products))

    for orderId in orderIds:
        rand = random.randint(1, 100)
        if rand <= 20:
            updateOrderStatusQuery(orderId, "cancelled")
        elif rand <= 45:
            updateOrderStatusQuery(orderId, "transit")
        elif rand <= 85:
            updateOrderStatusQuery(orderId, "fulfilled")

import requests
from src.app import app
from threading import Thread
from tests.helper import delete_user


def test_endpoint_authentication():
    # spin up server on a daemon thread
    server = Thread(target=app.run, kwargs={"port": 3001})
    server.daemon = True
    server.start()

    # register a user
    register_url = "http://localhost:3001/account/register"
    user_details = {
        "username": "auth_test",
        "password": "password",
        "email": "testemail@email.com",
    }

    response = requests.post(url=register_url, json=user_details)
    assert response.json() == {"msg": "Registration success"}

    # login and get access token
    login_url = "http://localhost:3001/account/login"
    login_details = {"username": "auth_test", "password": "password"}

    response = requests.post(url=login_url, json=login_details)
    responsejson = response.json()
    assert responsejson["msg"] == "Authentication success"
    assert "access_token" in responsejson

    access_token = responsejson["access_token"]

    # test token valid identity resolution
    hello_url = "http://localhost:3001/hello"
    response = requests.get(
        url=hello_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    responsejson = response.json()

    assert "data" in responsejson
    assert "greeting" in responsejson["data"]
    assert (
        "Hello, auth_test. Your token was created at"
        in responsejson["data"]["greeting"]
    )

    # test fail on invalid token
    spoof_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    response = requests.get(
        url=hello_url, headers={"Authorization": f"Bearer {spoof_token}"}
    )
    assert response.status_code == 422
    assert response.json() == {"msg": "Signature verification failed"}

    # try get data
    data_url = "http://localhost:3001/inventory"
    response = requests.get(
        url=data_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.json() == {"data": {"inventory": []}}

    # try get data without token
    data_url = "http://localhost:3001/inventory"
    response = requests.get(url=data_url)
    assert response.status_code == 401

    delete_user("auth_test")

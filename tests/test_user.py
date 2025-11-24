def test_create_user_success(client):
    payload = {
        "name": "Gabriel",
        "email": "gabriel@test.com",
        "password": "123456",
        "registry": "",
        "phone": "47999118612"
    }
    response = client.post("/api/users/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "gabriel@test.com"

def test_create_user_existing_email_should_fail(client):
    payload = {
        "name": "Gabriel",
        "email": "gabriel@test.com",
        "password": "123456",
        "registry": "",
        "phone": "47999118612"
    }
    response = client.post("/api/users/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

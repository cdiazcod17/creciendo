import pytest

def test_set_active_baby_success(client):
    client.post("/auth/register", json={"full_name": "U1", "email": "u1@e.com", "password": "Password123"})
    login1 = client.post("/auth/login", data={"username": "u1@e.com", "password": "Password123"})
    token1 = login1.json()["access_token"]
    
    baby_res = client.post(
        "/babies/",
        json={"name": "Baby U1", "birth_date": "2024-01-01"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    baby_id = baby_res.json()["id"]
    
    # Set as active
    response = client.patch(
        "/auth/me/active-baby",
        json={"baby_id": baby_id},
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
    assert response.json()["active_baby_id"] == baby_id

def test_set_active_baby_unauthorized(client):
    # User 1 baby
    client.post("/auth/register", json={"full_name": "U1", "email": "u1@e.com", "password": "Password123"})
    login1 = client.post("/auth/login", data={"username": "u1@e.com", "password": "Password123"})
    token1 = login1.json()["access_token"]
    baby_res = client.post(
        "/babies/",
        json={"name": "Baby U1", "birth_date": "2024-01-01"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    baby_id = baby_res.json()["id"]
    
    # User 2 tries to set User 1's baby as active
    client.post("/auth/register", json={"full_name": "U2", "email": "u2@e.com", "password": "Password123"})
    login2 = client.post("/auth/login", data={"username": "u2@e.com", "password": "Password123"})
    token2 = login2.json()["access_token"]
    
    response = client.patch(
        "/auth/me/active-baby",
        json={"baby_id": baby_id},
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404

import pytest

def test_baby_ownership(client):
    # User 1 registers and creates a baby
    client.post("/auth/register", json={"full_name": "U1", "email": "u1@e.com", "password": "Password123"})
    login1 = client.post("/auth/login", data={"username": "u1@e.com", "password": "Password123"})
    token1 = login1.json()["access_token"]
    
    baby_res = client.post(
        "/babies/",
        json={"name": "Baby U1", "birth_date": "2024-01-01"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    baby_id = baby_res.json()["id"]
    
    # User 2 registers
    client.post("/auth/register", json={"full_name": "U2", "email": "u2@e.com", "password": "Password123"})
    login2 = client.post("/auth/login", data={"username": "u2@e.com", "password": "Password123"})
    token2 = login2.json()["access_token"]
    
    # User 2 tries to access User 1's baby
    response = client.get(
        f"/babies/{baby_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404 # Should be 404 as per our validate_baby_ownership logic (not found or no permission)

def test_event_ownership(client):
    # User 1 registers and creates a baby and an event
    client.post("/auth/register", json={"full_name": "U1", "email": "u1@e.com", "password": "Password123"})
    login1 = client.post("/auth/login", data={"username": "u1@e.com", "password": "Password123"})
    token1 = login1.json()["access_token"]
    
    baby_res = client.post(
        "/babies/",
        json={"name": "Baby U1", "birth_date": "2024-01-01"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    baby_id = baby_res.json()["id"]
    
    event_res = client.post(
        f"/babies/{baby_id}/events/",
        json={"event_type": "feeding", "occurred_at": "2024-04-22T10:00:00"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    event_id = event_res.json()["id"]
    
    # User 2 tries to access User 1's event
    client.post("/auth/register", json={"full_name": "U2", "email": "u2@e.com", "password": "Password123"})
    login2 = client.post("/auth/login", data={"username": "u2@e.com", "password": "Password123"})
    token2 = login2.json()["access_token"]
    
    response = client.get(
        f"/babies/{baby_id}/events/{event_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404

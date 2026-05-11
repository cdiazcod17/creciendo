import pytest
from unittest.mock import patch
from app.models.password_reset import PasswordResetToken
from sqlalchemy import select

def test_password_reset_flow(client, db):
    # 1. Register a user
    client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "OldPassword123"
        }
    )

    # 2. Request password reset
    with patch("resend.Emails.send") as mock_send:
        response = client.post(
            "/auth/forgot-password",
            json={"email": "test@example.com"}
        )
        assert response.status_code == 200
        assert mock_send.called

    # 3. Get the token from the database
    token_obj = db.execute(select(PasswordResetToken)).scalar_one()
    token = token_obj.token

    # 4. Reset password
    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword123"
        }
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Contraseña actualizada exitosamente."

    # 5. Verify login with new password
    login_response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "NewPassword123"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    # 6. Verify old password doesn't work
    login_response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "OldPassword123"}
    )
    assert login_response.status_code == 401

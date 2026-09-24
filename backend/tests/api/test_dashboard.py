from fastapi import status

from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole
from app.infrastructure.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from app.infrastructure.security.jwt_token_service import JwtTokenService


def test_get_dashboard_without_authentication(client):
    response = client.get("/dashboard/summary")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_dashboard_as_admin(client, db_session):
    user_repository = PostgresUserRepository(db_session)

    admin = user_repository.create(
        User(
            id=None,
            name="Dashboard Admin",
            email="dashboard.admin@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(admin.id)
    )

    response = client.get(
        "/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

def test_get_dashboard_with_nonexistent_user(client):
    token = JwtTokenService().create_access_token(
        subject="999999999"
    )

    response = client.get(
        "/dashboard/summary",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == (
        "Invalid or expired token"
    )

def test_get_dashboard_with_inactive_user(client, db_session):
    user_repository = PostgresUserRepository(db_session)

    inactive_user = user_repository.create(
        User(
            id=None,
            name="Inactive Dashboard User",
            email="dashboard.inactive@test.com",
            hashed_password="test_password_hash",
            role=UserRole.ADMIN,
            is_active=False,
        )
    )

    token = JwtTokenService().create_access_token(
        subject=str(inactive_user.id)
    )

    response = client.get(
        "/dashboard/summary",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == (
        "Invalid or expired token"
    )

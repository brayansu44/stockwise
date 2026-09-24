from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "StockWise API funcionando correctamente"
    )
    assert data["status"] == "ok"
    assert "environment" in data

def test_health_check():
    # Act
    response = client.get("/health/")

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["message"] == "StockWise API is running"

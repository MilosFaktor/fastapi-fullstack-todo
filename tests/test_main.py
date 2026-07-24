from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_return_health_chekc():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}

"""
Automated tests for the Animal Picture App.

These tests use FastAPI's TestClient with a separate test database,
and mock the external API calls so tests run fast and don't depend
on placekitten.com / place.dog / placebear.com being reachable.
"""
import os
import sys
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use a separate, disposable test database
os.environ["TESTING"] = "1"

from app.main import app
from app.database import init_db, SessionLocal, AnimalPicture, engine, Base


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """Fresh database for every test."""
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up all rows after each test so tests don't interfere with each other
    db = SessionLocal()
    db.query(AnimalPicture).delete()
    db.commit()
    db.close()


@pytest.fixture
def client():
    return TestClient(app)


class TestFetchEndpoint:
    """Tests for POST /animals/fetch"""

    @patch("app.main.fetch_multiple_animal_images", new_callable=AsyncMock)
    def test_fetch_single_picture_success(self, mock_fetch, client):
        mock_fetch.return_value = [("https://place.dog/300/300", "./app/images/dog_abc123.jpg")]

        response = client.post("/animals/fetch", json={"animal_type": "dog", "count": 1})

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["animal_type"] == "dog"
        assert data[0]["source_url"] == "https://place.dog/300/300"

    @patch("app.main.fetch_multiple_animal_images", new_callable=AsyncMock)
    def test_fetch_multiple_pictures(self, mock_fetch, client):
        mock_fetch.return_value = [
            ("https://placekitten.com/300/300", "./app/images/cat_1.jpg"),
            ("https://placekitten.com/300/300", "./app/images/cat_2.jpg"),
            ("https://placekitten.com/300/300", "./app/images/cat_3.jpg"),
        ]

        response = client.post("/animals/fetch", json={"animal_type": "cat", "count": 3})

        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_fetch_invalid_animal_type(self, client):
        from app.animal_service import UnsupportedAnimalError

        with patch("app.main.fetch_multiple_animal_images", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.side_effect = UnsupportedAnimalError("'elephant' is not supported")
            response = client.post("/animals/fetch", json={"animal_type": "elephant", "count": 1})

        assert response.status_code == 400

    def test_fetch_count_out_of_range(self, client):
        response = client.post("/animals/fetch", json={"animal_type": "dog", "count": 0})
        assert response.status_code == 422  # Pydantic validation error

        response = client.post("/animals/fetch", json={"animal_type": "dog", "count": 11})
        assert response.status_code == 422


class TestLatestEndpoint:
    """Tests for GET /animals/{animal_type}/latest"""

    def test_get_latest_no_records_returns_404(self, client):
        response = client.get("/animals/cat/latest")
        assert response.status_code == 404

    def test_get_latest_returns_most_recent_record(self, client):
        db = SessionLocal()
        db.add(AnimalPicture(animal_type="bear", source_url="url1", file_path="path1.jpg"))
        db.add(AnimalPicture(animal_type="bear", source_url="url2", file_path="path2.jpg"))
        db.commit()
        db.close()

        response = client.get("/animals/bear/latest")

        assert response.status_code == 200
        # Should return the second (most recently inserted) record
        assert response.json()["source_url"] == "url2"

    def test_get_latest_is_case_insensitive(self, client):
        db = SessionLocal()
        db.add(AnimalPicture(animal_type="cat", source_url="url1", file_path="path1.jpg"))
        db.commit()
        db.close()

        response = client.get("/animals/CAT/latest")
        assert response.status_code == 200

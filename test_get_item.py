"""
Тесты для получения объявления по идентификатору (GET /api/1/item/{id})
"""
import pytest
import requests


class TestGetItem:
    """Тесты для эндпоинта получения объявления по id"""

    BASE_URL = "https://qa-internship.avito.com"
    API_VERSION = "1"

    @pytest.fixture
    def endpoint(self, created_item):
        item_id = created_item["id"]
        return f"{self.BASE_URL}/api/{self.API_VERSION}/item/{item_id}"

    def test_get_item_success(self, endpoint, created_item):
        """TC-2.1: Успешное получение существующего объявления"""
        response = requests.get(
            endpoint,
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        
        data = response.json()
        # API возвращает массив
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 0, "Response array should not be empty"
        
        item = data[0]
        
        # Проверка обязательных полей
        required_fields = ["id", "sellerId", "name", "price", "statistics", "createdAt"]
        for field in required_fields:
            assert field in item, f"Field '{field}' is missing in response"

        # Проверка соответствия данных
        assert item["id"] == created_item["id"], "id should match"
        assert item["sellerId"] == created_item["sellerId"], "sellerId should match"
        assert item["name"] == created_item["name"], "name should match"
        assert item["price"] == created_item["price"], "price should match"
        assert item["statistics"] == created_item["statistics"], "statistics should match"

    def test_get_nonexistent_item(self):
        """TC-2.2: Получение несуществующего объявления"""
        response = requests.get(
            f"{self.BASE_URL}/api/{self.API_VERSION}/item/nonexistent-id-12345",
            headers={"Accept": "application/json"}
        )

        # API возвращает 400 вместо 404 для некорректного формата id
        assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}. Response: {response.text}"
        
        error_data = response.json()
        assert "result" in error_data, "Response should contain 'result' field"
        assert "status" in error_data, "Response should contain 'status' field"

    def test_get_item_with_invalid_id_format(self):
        """TC-2.4: Получение объявления с некорректным форматом id"""
        response = requests.get(
            f"{self.BASE_URL}/api/{self.API_VERSION}/item/!@#$%^&*()",
            headers={"Accept": "application/json"}
        )

        # Может быть 400 или 404
        assert response.status_code in [400, 404], f"Unexpected status code: {response.status_code}"


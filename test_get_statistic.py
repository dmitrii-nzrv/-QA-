"""
Тесты для получения статистики по объявлению (GET /api/1/statistic/{id})
"""
import pytest
import requests


class TestGetStatistic:
    """Тесты для эндпоинта получения статистики по объявлению"""

    BASE_URL = "https://qa-internship.avito.com"
    API_VERSION = "1"

    @pytest.fixture
    def endpoint(self, created_item):
        item_id = created_item["id"]
        return f"{self.BASE_URL}/api/{self.API_VERSION}/statistic/{item_id}"

    def test_get_statistic_success(self, endpoint, created_item):
        """TC-4.1: Успешное получение статистики существующего объявления"""
        response = requests.get(
            endpoint,
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 0, "Response array should not be empty"
        
        statistic = data[0] if data[0] is not None else {}
        
        # Проверка обязательных полей статистики
        required_fields = ["likes", "viewCount", "contacts"]
        for field in required_fields:
            assert field in statistic, f"Field '{field}' is missing in statistic"
        
        # Проверка соответствия значений
        expected_stats = created_item["statistics"]
        assert statistic["likes"] == expected_stats["likes"], "likes should match"
        assert statistic["viewCount"] == expected_stats["viewCount"], "viewCount should match"
        assert statistic["contacts"] == expected_stats["contacts"], "contacts should match"

    def test_get_statistic_nonexistent_item(self):
        """TC-4.2: Получение статистики несуществующего объявления"""
        response = requests.get(
            f"{self.BASE_URL}/api/{self.API_VERSION}/statistic/nonexistent-id-12345",
            headers={"Accept": "application/json"}
        )

        # API возвращает 400 вместо 404 для некорректного id
        assert response.status_code in [400, 404], f"Expected 400 or 404, got {response.status_code}. Response: {response.text}"
        
        error_data = response.json()
        assert "result" in error_data, "Response should contain 'result' field"
        assert "status" in error_data, "Response should contain 'status' field"

    def test_get_statistic_with_invalid_id_format(self):
        """TC-4.4: Получение статистики с некорректным форматом id"""
        response = requests.get(
            f"{self.BASE_URL}/api/{self.API_VERSION}/statistic/!@#$%^&*()",
            headers={"Accept": "application/json"}
        )

        # Может быть 400 или 404
        assert response.status_code in [400, 404], f"Unexpected status code: {response.status_code}"


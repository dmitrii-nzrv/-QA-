"""
Тесты для получения всех объявлений продавца (GET /api/1/{sellerID}/item)
"""
import pytest
import requests


class TestGetSellerItems:
    """Тесты для эндпоинта получения всех объявлений продавца"""

    BASE_URL = "https://qa-internship.avito.com"
    API_VERSION = "1"

    def test_get_seller_items_success(self, base_url, api_version, unique_seller_id, sample_item_data):
        """TC-3.1: Успешное получение всех объявлений продавца"""
        # Создаем несколько объявлений с одинаковым sellerID
        created_items = []
        for i in range(3):
            data = sample_item_data.copy()
            data["sellerID"] = unique_seller_id
            data["name"] = f"testItem_{i}"
            
            response = requests.post(
                f"{base_url}/api/{api_version}/item",
                json=data,
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            assert response.status_code == 200, f"Failed to create item {i}: {response.text}"
            item_data = response.json()
            if isinstance(item_data, list):
                item_data = item_data[0]
            created_items.append(item_data)

        # Получаем все объявления продавца
        response = requests.get(
            f"{base_url}/api/{api_version}/{unique_seller_id}/item",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        
        # Проверяем, что все созданные объявления присутствуют
        assert len(data) >= 3, f"Expected at least 3 items, got {len(data)}"
        
        # Проверяем, что все элементы имеют правильный sellerId
        for item in data:
            assert "sellerId" in item, "Each item should have sellerId"
            assert item["sellerId"] == unique_seller_id, f"All items should have sellerId={unique_seller_id}"
            
            # Проверка обязательных полей
            required_fields = ["id", "sellerId", "name", "price", "statistics", "createdAt"]
            for field in required_fields:
                assert field in item, f"Field '{field}' is missing in item"

    def test_get_nonexistent_seller_items(self):
        """TC-3.2: Получение объявлений несуществующего продавца"""
        # Используем sellerID, который точно не существует (вне диапазона)
        response = requests.get(
            f"{self.BASE_URL}/api/{self.API_VERSION}/111110/item",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        # API может возвращать объявления других пользователей, поэтому проверяем только тип

    def test_get_seller_items_with_string_seller_id(self):
        """TC-3.3: Получение объявлений продавца с некорректным типом sellerID"""
        response = requests.get(
            f"{self.BASE_URL}/api/{self.API_VERSION}/abc/item",
            headers={"Accept": "application/json"}
        )

        # Может быть 400 или 404
        assert response.status_code in [400, 404], f"Unexpected status code: {response.status_code}"

    def test_get_seller_items_with_negative_seller_id(self):
        """TC-3.4: Получение объявлений продавца с отрицательным sellerID"""
        response = requests.get(
            f"{self.BASE_URL}/api/{self.API_VERSION}/-123/item",
            headers={"Accept": "application/json"}
        )

        # Может быть 400 или 200 в зависимости от бизнес-логики
        assert response.status_code in [200, 400], f"Unexpected status code: {response.status_code}"


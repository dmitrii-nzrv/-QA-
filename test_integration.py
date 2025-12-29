"""
Интеграционные тесты
"""
import pytest
import requests


class TestIntegration:
    """Интеграционные тесты для проверки взаимодействия эндпоинтов"""

    BASE_URL = "https://qa-internship.avito.com"
    API_VERSION = "1"

    def test_create_and_get_item(self, base_url, api_version, sample_item_data):
        """TC-5.1: Создание объявления и последующее получение его по id"""
        # Создаем объявление
        create_response = requests.post(
            f"{base_url}/api/{api_version}/item",
            json=sample_item_data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        
        assert create_response.status_code == 200, f"Failed to create item: {create_response.text}"
        created_item = create_response.json()
        
        # Обработка ответа API
        item_id = None
        if isinstance(created_item, dict):
            if "status" in created_item:
                status_text = created_item["status"]
                if " - " in status_text:
                    item_id = status_text.split(" - ")[-1]
            elif "id" in created_item:
                item_id = created_item["id"]
        elif isinstance(created_item, list) and len(created_item) > 0:
            if "id" in created_item[0]:
                item_id = created_item[0]["id"]
        
        assert item_id, f"Failed to extract item id from response: {created_item}"
        
        # Получаем объявление
        get_response = requests.get(
            f"{base_url}/api/{api_version}/item/{item_id}",
            headers={"Accept": "application/json"}
        )
        
        assert get_response.status_code == 200, f"Failed to get item: {get_response.text}"
        retrieved_items = get_response.json()
        assert isinstance(retrieved_items, list), "Response should be an array"
        assert len(retrieved_items) > 0, "Response should contain at least one item"
        
        retrieved_item = retrieved_items[0]
        
        # Проверяем соответствие данных
        assert retrieved_item["id"] == item_id, "id should match"
        assert retrieved_item["sellerId"] == sample_item_data["sellerID"], "sellerId should match"
        assert retrieved_item["name"] == sample_item_data["name"], "name should match"
        assert retrieved_item["price"] == sample_item_data["price"], "price should match"
        assert retrieved_item["statistics"] == sample_item_data["statistics"], "statistics should match"

    def test_create_multiple_items_and_get_all(self, base_url, api_version, unique_seller_id, sample_item_data):
        """TC-5.2: Создание нескольких объявлений одного продавца и получение всех его объявлений"""
        # Создаем 3 объявления с одинаковым sellerID
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
            
            # Обработка ответа API
            item_id = None
            if isinstance(item_data, dict):
                if "status" in item_data:
                    status_text = item_data["status"]
                    if " - " in status_text:
                        item_id = status_text.split(" - ")[-1]
                        # Получаем объявление по id
                        get_response = requests.get(
                            f"{base_url}/api/{api_version}/item/{item_id}",
                            headers={"Accept": "application/json"}
                        )
                        if get_response.status_code == 200:
                            items = get_response.json()
                            if isinstance(items, list) and len(items) > 0:
                                item_data = items[0]
                elif "id" in item_data:
                    item_id = item_data["id"]
            elif isinstance(item_data, list) and len(item_data) > 0:
                item_data = item_data[0]
                if "id" in item_data:
                    item_id = item_data["id"]
            
            if item_id and "id" in item_data:
                created_items.append(item_data)
        
        # Получаем все объявления продавца
        get_response = requests.get(
            f"{base_url}/api/{api_version}/{unique_seller_id}/item",
            headers={"Accept": "application/json"}
        )
        
        assert get_response.status_code == 200, f"Failed to get seller items: {get_response.text}"
        retrieved_items = get_response.json()
        assert isinstance(retrieved_items, list), "Response should be an array"
        
        # Проверяем, что все созданные объявления присутствуют
        created_ids = {item["id"] for item in created_items}
        retrieved_ids = {item["id"] for item in retrieved_items}
        
        assert created_ids.issubset(retrieved_ids), "All created items should be in the response"
        
        # Проверяем, что все элементы имеют правильный sellerId
        for item in retrieved_items:
            assert item["sellerId"] == unique_seller_id, f"All items should have sellerId={unique_seller_id}"

    def test_create_item_and_get_statistic(self, base_url, api_version, sample_item_data):
        """TC-5.3: Создание объявления и получение его статистики"""
        # Создаем объявление
        create_response = requests.post(
            f"{base_url}/api/{api_version}/item",
            json=sample_item_data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        
        assert create_response.status_code == 200, f"Failed to create item: {create_response.text}"
        created_item = create_response.json()
        
        # Обработка ответа API
        item_id = None
        if isinstance(created_item, dict):
            if "status" in created_item:
                status_text = created_item["status"]
                if " - " in status_text:
                    item_id = status_text.split(" - ")[-1]
            elif "id" in created_item:
                item_id = created_item["id"]
        elif isinstance(created_item, list) and len(created_item) > 0:
            if "id" in created_item[0]:
                item_id = created_item[0]["id"]
        
        assert item_id, f"Failed to extract item id from response: {created_item}"
        expected_stats = sample_item_data["statistics"]
        
        # Получаем статистику
        stat_response = requests.get(
            f"{base_url}/api/{api_version}/statistic/{item_id}",
            headers={"Accept": "application/json"}
        )
        
        assert stat_response.status_code == 200, f"Failed to get statistic: {stat_response.text}"
        statistic_data = stat_response.json()
        assert isinstance(statistic_data, list), "Response should be an array"
        assert len(statistic_data) > 0, "Response should contain statistic"
        
        statistic = statistic_data[0] if statistic_data[0] is not None else {}
        
        # Проверяем соответствие статистики
        assert statistic["likes"] == expected_stats["likes"], "likes should match"
        assert statistic["viewCount"] == expected_stats["viewCount"], "viewCount should match"
        assert statistic["contacts"] == expected_stats["contacts"], "contacts should match"


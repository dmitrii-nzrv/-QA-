"""
Тесты для создания объявлений (POST /api/1/item)
"""
import pytest
import requests


class TestCreateItem:
    """Тесты для эндпоинта создания объявлений"""

    BASE_URL = "https://qa-internship.avito.com"
    API_VERSION = "1"

    @pytest.fixture
    def endpoint(self):
        return f"{self.BASE_URL}/api/{self.API_VERSION}/item"

    def test_create_item_success(self, endpoint, sample_item_data):
        """TC-1.1: Успешное создание объявления со всеми обязательными полями"""
        response = requests.post(
            endpoint,
            json=sample_item_data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        
        data = response.json()
        
        # API может возвращать объект с полем "status" или объект с данными
        item_id = None
        if isinstance(data, dict):
            if "status" in data:
                # Извлекаем id из строки статуса: "Сохранили объявление - {id}"
                status_text = data["status"]
                if " - " in status_text:
                    item_id = status_text.split(" - ")[-1]
                    # Получаем объявление по id для проверки
                    get_response = requests.get(
                        f"{self.BASE_URL}/api/{self.API_VERSION}/item/{item_id}",
                        headers={"Accept": "application/json"}
                    )
                    if get_response.status_code == 200:
                        items = get_response.json()
                        if isinstance(items, list) and len(items) > 0:
                            item = items[0]
                        else:
                            item = data
                    else:
                        item = data
                else:
                    item = data
            elif "id" in data:
                item = data
            else:
                item = data
        elif isinstance(data, list) and len(data) > 0:
            item = data[0]
        else:
            item = data

        # Если получили только id из status, проверяем что id не пустой
        if item_id:
            assert item_id, "id should not be empty"
            # Проверяем, что получили объявление
            assert "id" in item, f"Failed to retrieve created item. Response: {item}"
        
        # Проверка обязательных полей (если они есть в ответе)
        if "id" in item:
            assert isinstance(item["id"], str), "id should be a string"
            assert item["id"], "id should not be empty"
        
        # Проверяем наличие полей, если они есть в ответе
        if "sellerId" in item:
            assert item["sellerId"] == sample_item_data["sellerID"], "sellerId should match sellerID"
        if "name" in item:
            assert item["name"] == sample_item_data["name"], "name should match"
        if "price" in item:
            assert item["price"] == sample_item_data["price"], "price should match"
        
        # Проверка statistics
        if "statistics" in item:
            stats = item["statistics"]
            assert stats["likes"] == sample_item_data["statistics"]["likes"]
            assert stats["viewCount"] == sample_item_data["statistics"]["viewCount"]
            assert stats["contacts"] == sample_item_data["statistics"]["contacts"]
        
        if "createdAt" in item:
            assert isinstance(item["createdAt"], str), "createdAt should be a string"
            assert item["createdAt"], "createdAt should not be empty"

    def test_create_item_without_seller_id(self, endpoint, sample_item_data):
        """TC-1.2: Создание объявления без обязательного поля sellerID"""
        data = sample_item_data.copy()
        del data["sellerID"]
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        
        error_data = response.json()
        assert "result" in error_data, "Response should contain 'result' field"
        assert "status" in error_data, "Response should contain 'status' field"

    def test_create_item_without_name(self, endpoint, sample_item_data):
        """TC-1.3: Создание объявления без обязательного поля name"""
        data = sample_item_data.copy()
        del data["name"]
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        
        error_data = response.json()
        assert "result" in error_data, "Response should contain 'result' field"
        assert "status" in error_data, "Response should contain 'status' field"

    def test_create_item_without_price(self, endpoint, sample_item_data):
        """TC-1.4: Создание объявления без обязательного поля price"""
        data = sample_item_data.copy()
        del data["price"]
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        
        error_data = response.json()
        assert "result" in error_data, "Response should contain 'result' field"
        assert "status" in error_data, "Response should contain 'status' field"

    def test_create_item_without_statistics(self, endpoint, sample_item_data):
        """TC-1.5: Создание объявления без обязательного поля statistics"""
        data = sample_item_data.copy()
        del data["statistics"]
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        
        error_data = response.json()
        assert "result" in error_data, "Response should contain 'result' field"
        assert "status" in error_data, "Response should contain 'status' field"

    def test_create_item_without_likes(self, endpoint, sample_item_data):
        """TC-1.6: Создание объявления с неполной статистикой (без likes)"""
        data = sample_item_data.copy()
        del data["statistics"]["likes"]
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"

    def test_create_item_without_view_count(self, endpoint, sample_item_data):
        """TC-1.7: Создание объявления с неполной статистикой (без viewCount)"""
        data = sample_item_data.copy()
        del data["statistics"]["viewCount"]
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"

    def test_create_item_without_contacts(self, endpoint, sample_item_data):
        """TC-1.8: Создание объявления с неполной статистикой (без contacts)"""
        data = sample_item_data.copy()
        del data["statistics"]["contacts"]
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"

    def test_create_item_with_string_seller_id(self, endpoint, sample_item_data):
        """TC-1.9: Создание объявления с некорректным типом данных для sellerID"""
        data = sample_item_data.copy()
        data["sellerID"] = "not_a_number"
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"

    def test_create_item_with_string_price(self, endpoint, sample_item_data):
        """TC-1.10: Создание объявления с некорректным типом данных для price"""
        data = sample_item_data.copy()
        data["price"] = "not_a_number"
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"

    def test_create_item_with_negative_price(self, endpoint, sample_item_data):
        """TC-1.11: Создание объявления с отрицательным значением price"""
        data = sample_item_data.copy()
        data["price"] = -100
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        
        # Может быть 200 или 400 в зависимости от бизнес-логики
        assert response.status_code in [200, 400], f"Unexpected status code: {response.status_code}"

    def test_create_item_with_empty_name(self, endpoint, sample_item_data):
        """TC-1.12: Создание объявления с пустой строкой в name"""
        data = sample_item_data.copy()
        data["name"] = ""
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        
        # Может быть 200 или 400 в зависимости от бизнес-логики
        assert response.status_code in [200, 400], f"Unexpected status code: {response.status_code}"

    def test_create_item_with_min_seller_id(self, endpoint, sample_item_data):
        """TC-6.1: Создание объявления с минимальным sellerID (111111)"""
        data = sample_item_data.copy()
        data["sellerID"] = 111111
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

    def test_create_item_with_max_seller_id(self, endpoint, sample_item_data):
        """TC-6.2: Создание объявления с максимальным sellerID (999999)"""
        data = sample_item_data.copy()
        data["sellerID"] = 999999
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

    def test_create_item_with_zero_price(self, endpoint, sample_item_data):
        """TC-6.3: Создание объявления с нулевым price"""
        data = sample_item_data.copy()
        data["price"] = 0
        
        response = requests.post(
            endpoint,
            json=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        
        # Может быть 200 или 400 в зависимости от бизнес-логики
        assert response.status_code in [200, 400], f"Unexpected status code: {response.status_code}"


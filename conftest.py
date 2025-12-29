"""
Конфигурация для pytest тестов
"""
import pytest
import random
import requests

BASE_URL = "https://qa-internship.avito.com"
API_VERSION = "1"


@pytest.fixture
def base_url():
    """Базовый URL API"""
    return BASE_URL


@pytest.fixture
def api_version():
    """Версия API"""
    return API_VERSION


@pytest.fixture
def unique_seller_id():
    """Генерация уникального sellerID в диапазоне 111111-999999"""
    return random.randint(111111, 999999)


@pytest.fixture
def sample_item_data(unique_seller_id):
    """Пример данных для создания объявления"""
    return {
        "sellerID": unique_seller_id,
        "name": "testItem",
        "price": 9900,
        "statistics": {
            "likes": 21,
            "viewCount": 11,
            "contacts": 43
        }
    }


def extract_item_id_from_response(response_data, base_url, api_version):
    """Извлекает id объявления из ответа API и получает полные данные"""
    item_id = None
    
    if isinstance(response_data, dict):
        if "status" in response_data:
            # API возвращает {"status": "Сохранили объявление - {id}"}
            status_text = response_data["status"]
            if " - " in status_text:
                item_id = status_text.split(" - ")[-1]
        elif "id" in response_data:
            item_id = response_data["id"]
    elif isinstance(response_data, list) and len(response_data) > 0:
        if "id" in response_data[0]:
            item_id = response_data[0]["id"]
    
    # Если получили id, получаем полные данные объявления
    if item_id:
        get_response = requests.get(
            f"{base_url}/api/{api_version}/item/{item_id}",
            headers={"Accept": "application/json"}
        )
        if get_response.status_code == 200:
            items = get_response.json()
            if isinstance(items, list) and len(items) > 0:
                return items[0]
    
    return response_data


@pytest.fixture
def created_item(base_url, api_version, sample_item_data):
    """Создает объявление и возвращает его данные"""
    response = requests.post(
        f"{base_url}/api/{api_version}/item",
        json=sample_item_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 200, f"Failed to create item: {response.text}"
    response_data = response.json()
    
    # Извлекаем id и получаем полные данные
    item_data = extract_item_id_from_response(response_data, base_url, api_version)
    
    # Проверяем, что есть id
    assert "id" in item_data, f"Response doesn't contain 'id': {item_data}"
    yield item_data
    # Cleanup не требуется, так как нет DELETE endpoint в версии 1

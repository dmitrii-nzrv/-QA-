# Тестовое задание QA - Автоматизация тестирования API

## Автор
Назаров Дмитрий Алексеевич  
31.01.2003

## Описание проекта

Проект содержит автоматизированные тесты для API микросервиса объявлений Avito.

**Base URL:** https://qa-internship.avito.com  

### Эндпоинты API:
1. `POST /api/1/item` - Создание объявления
2. `GET /api/1/item/{id}` - Получение объявления по идентификатору
3. `GET /api/1/{sellerID}/item` - Получение всех объявлений продавца
4. `GET /api/1/statistic/{id}` - Получение статистики по объявлению

## Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

## Установка

1. Клонируйте репозиторий или скачайте файлы проекта

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Структура проекта

```
Тестовое_QA_Avito/
├── README.md                    # Инструкция по запуску (этот файл)
├── TESTCASES.md                 # Описание всех тест-кейсов
├── BUGS.md                      # Баг-репорты найденных проблем
├── requirements.txt             # Зависимости проекта
├── conftest.py                  # Конфигурация pytest и фикстуры
├── test_create_item.py          # Тесты для создания объявлений
├── test_get_item.py             # Тесты для получения объявления по id
├── test_get_seller_items.py     # Тесты для получения объявлений продавца
├── test_get_statistic.py        # Тесты для получения статистики
└── test_integration.py          # Интеграционные тесты
```

## Запуск тестов

### Запуск всех тестов

```bash
pytest
```

### Запуск конкретного файла с тестами

```bash
# Тесты создания объявлений
pytest test_create_item.py

# Тесты получения объявления
pytest test_get_item.py

# Тесты получения объявлений продавца
pytest test_get_seller_items.py

# Тесты получения статистики
pytest test_get_statistic.py

# Интеграционные тесты
pytest test_integration.py
```

### Запуск конкретного теста

```bash
pytest test_create_item.py::TestCreateItem::test_create_item_success
```

### Запуск с подробным выводом

```bash
pytest -v
```

### Запуск с выводом print-ов

```bash
pytest -s
```

### Запуск с генерацией HTML отчета

```bash
pytest --html=report.html --self-contained-html
```

После выполнения команды будет создан файл `report.html` с подробным отчетом о тестировании.

### Запуск с остановкой на первой ошибке

```bash
pytest -x
```

### Запуск с максимальным количеством упавших тестов

```bash
pytest --maxfail=5
```

---

## Примеры запуска

### Базовый запуск всех тестов:
```bash
pytest
```

### Запуск с подробным выводом и HTML отчетом:
```bash
pytest -v --html=report.html --self-contained-html
```

### Запуск только критичных тестов (High priority):
```bash
pytest -v -k "test_create_item_success or test_get_item_success or test_get_seller_items_success or test_get_statistic_success"
```

## Результаты тестирования

После выполнения тестов вы увидите:
- Количество пройденных тестов
- Количество упавших тестов
- Детальную информацию об ошибках (если есть)
- Время выполнения тестов

Пример вывода:
```
========================= test session starts ==========================
collected 25 items

test_create_item.py::TestCreateItem::test_create_item_success PASSED
test_create_item.py::TestCreateItem::test_create_item_without_seller_id PASSED
...
========================= 25 passed in 15.23s ==========================
```

## Найденные баги

Все найденные баги задокументированы в файле `BUGS.md`.


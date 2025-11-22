# File Upload Endpoint Guide

## Обзор

Новый endpoint `/api/v1/upload` позволяет загружать файлы с кодом для проверки на плагиат. Это удобная альтернатива endpoint `/api/v1/check`, когда вы хотите проверить файл напрямую, а не отправлять код в JSON.

## Endpoint

**URL:** `POST /api/v1/upload`

**Content-Type:** `multipart/form-data`

**Параметры:**
- `file` (required) - Python файл для проверки (должен быть текстовым файлом с UTF-8 кодировкой)

## Примеры использования

### 1. Использование curl

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@example_code.py"
```

### 2. Использование Python requests

```python
import requests

# Загрузка файла
with open('example_code.py', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/upload', files=files)
    result = response.json()

# Обработка результата
if result['success']:
    for comparison in result['comparisons']:
        print(f"Block: {comparison['block_name']}")
        print(f"Similarity: {comparison['similarity_percent']}%")
        if comparison['source_repo']:
            print(f"Source: {comparison['source_repo']}")
        print()
```

### 3. Использование тестового скрипта

Мы предоставляем готовый скрипт для тестирования:

```bash
python test_upload_endpoint.py example_code.py
```

## Формат ответа

Endpoint возвращает тот же формат ответа, что и `/api/v1/check`:

```json
{
  "success": true,
  "comparisons": [
    {
      "block_name": "fibonacci",
      "similarity_percent": 85,
      "source_repo": "github.com/user/repo",
      "source_url": "https://github.com/user/repo/blob/main/file.py",
      "reason": "Very similar recursive implementation"
    }
  ]
}
```

## Обработка ошибок

### 400 Bad Request

**Пустой файл:**
```json
{
  "detail": "File is empty or contains no code"
}
```

**Неверная кодировка:**
```json
{
  "detail": "File must be a text file with UTF-8 encoding"
}
```

**Файл не предоставлен:**
```json
{
  "detail": "No file provided"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Error message..."
}
```

## Логика обработки

Endpoint выполняет следующие шаги:

1. **Валидация файла** - проверяет, что файл предоставлен
2. **Чтение содержимого** - декодирует файл в UTF-8
3. **Проверка на пустоту** - убеждается, что файл содержит код
4. **Запуск pipeline** - использует тот же Orchestrator, что и `/api/v1/check`:
   - Agent 1: Code Splitter - разбивает код на блоки (функции/классы)
   - Agent 2: Git Searcher - ищет похожий код на GitHub
   - Agent 3: Similarity Finder - сравнивает блоки с помощью LLM
5. **Форматирование ответа** - возвращает результаты в стандартном формате

## Сравнение с /api/v1/check

| Характеристика | /api/v1/check | /api/v1/upload |
|---------------|---------------|----------------|
| Формат входных данных | JSON с полем "code" | Multipart file upload |
| Использование | Для проверки фрагментов кода | Для проверки целых файлов |
| Content-Type | application/json | multipart/form-data |
| Обработка | Та же самая pipeline | Та же самая pipeline |
| Формат ответа | Идентичный | Идентичный |

## Примеры файлов для тестирования

Вы можете использовать `example_code.py` для тестирования endpoint:

```python
# example_code.py
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## Swagger UI

Endpoint также доступен через Swagger UI:

```
http://localhost:8000/docs
```

В Swagger UI вы можете:
- Протестировать endpoint интерактивно
- Загрузить файл через веб-интерфейс
- Просмотреть схемы запроса/ответа
- Увидеть примеры использования

## Ограничения

- Файл должен быть текстовым с UTF-8 кодировкой
- Рекомендуется использовать Python файлы (.py)
- Большие файлы могут занять больше времени на обработку
- Применяются те же ограничения GitHub API и OpenAI API, что и для `/api/v1/check`

## Техническая реализация

### Файл: `app/api/v1/endpoints/upload.py`

Endpoint реализован как async функция FastAPI:

```python
@router.post("/upload", response_model=CheckResponse)
async def check_code_from_file(file: UploadFile = File(...)):
    # Валидация и чтение файла
    content = await file.read()
    code = content.decode('utf-8')
    
    # Выполнение pipeline
    result = orchestrator.execute_pipeline(code)
    
    # Возврат результата
    return CheckResponse(...)
```

### Интеграция в роутер

Endpoint добавлен в `app/api/v1/router.py`:

```python
from app.api.v1.endpoints import health, check, upload

router.include_router(upload.router, tags=["plagiarism"])
```

## Поддержка

Для вопросов и проблем:
- Проверьте логи сервера
- Убедитесь, что API ключи настроены правильно
- Используйте тестовый скрипт для отладки


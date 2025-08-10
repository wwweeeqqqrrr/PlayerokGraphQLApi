# API запросов Playerok от Kioke

API является комплексным решением для продавца,в нем есть все функции для простого использования или дальнейшей разработки:

## Установка

Для использования API запросов Playerok установите необходимые зависимости:

```bash
pip install wrapper-tls-requests==1.1.2
```

Разместите ваши cookies в файле `cookies.json` или укажите пользовательский путь при инициализации классов API.

## Начало работы

1. **Инициализация класса API**:
   ```python
   from api import KiokePlayerok
   useApi = KiokePlayerok(cookies_file="cookies.json",username="вашникнеймнасайте")
   ```

2. **Пример использования** (получение числа активных):
   ```python
   countDeals = useApi.get_actual_deals()
   if countDeals > 0:
      print("Новая сделка!")
   ```


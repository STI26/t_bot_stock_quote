## IEXStockQuoteBot
---
Телеграм бот позволяющий получать текущие цены на акции торгующиеся на IEX Group inc. 
При помощи IEX Cloud Financial Data API.

Установка:

- git clon https://github.com/STI26/t_bot_stock_quote.git
- pip install -r requirements.txt
- переименовываем configuration.example.py в configuration.py
- регистрируемся https://iexcloud.io/cloud-login#/register/
- полученный токен копируем в configuration.py
- создаём телеграм бота
- полученный токен копируем в configuration.py
- загружаем на сервер
- устанавливаем webhook телеграма при помощи setWebhook метода
- запускаем application.py

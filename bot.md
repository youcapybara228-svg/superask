# Деплой Telegram-бота Super ASK на Render

## 1. Подготовка

1. Убедитесь, что проект загружен в Git-репозиторий (GitHub/GitLab).

2. В файле `requirements.txt` должны быть указаны зависимости:
   ```
   aiogram>=3.18.0,<4.0.0
   cryptography>=42.0.0
   python-dotenv>=1.0.0
   ```

## 2. Создание Web Service на Render

1. Зайдите в [Render Dashboard](https://dashboard.render.com).
2. Нажмите **New + → Web Service**.
3. Подключите ваш Git-репозиторий.
4. Настройте:
   - **Name**: `superask-bot` (или любое другое)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m src.main`

## 3. Переменные окружения

В разделе **Environment Variables** добавьте:

| Variable | Значение |
|---|---|
| `BOT_TOKEN` | Токен вашего Telegram-бота (от @BotFather) |
| `ADMIN_USER_ID` | Ваш Telegram User ID (узнать у @userinfobot) |
| `ENCRYPTION_KEY` | Ключ шифрования: выполнить `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |

## 4. Деплой

Нажмите **Deploy**. Render автоматически:
- Установит зависимости
- Запустит бота
- Перезапустит при падении (Restart Policy)

## 5. Мониторинг

- **Логи**: Render Dashboard → ваш сервис → **Logs**
- **Перезапуск**: Render автоматически перезапускает при падении
- **Uptime**: Можно подключить платный план для 100% аптайма

## 6. Важные замечания

- Render бесплатный план "спит" через 15 минут бездействия. Telegram-бот может пропускать сообщения.
- Для продакшена рекомендуется **Starter** ($7/мес) или выше.
- Команды `/SA userid`, `/SA bot` и `/SA model` работают **только через локальный терминал**, не через Render.
- SUA-компонент (sudo) работает только на вашем ПК, не на Render.

# Чат-бот для помощи службе поддержки

Чат-бот для ответов на часто задаваемые вопросы.

Код выполняет три задачи:
1) Отвечает на часто задаваемые вопросы в чат-боте в Телеграме.
2) Отвечает на часто задаваемые вопросы в чат-боте в VK (и не отвечает, если у него нет ответа на вопрос).
3) Бот обучается на готовых данных с помощью DialogFlow.

## Как установить

Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей.
`pip install -r requirements.txt`

Параметры `TELEGRAM_BOT_TOKEN`, `PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`, `VK_API_TOKEN` и `TELEGRAM_CHAT_ID` должны находится в файле `.env` рядом со скриптом.

Получить `TELEGRAM_BOT_TOKEN` можно в Telegram у @BotFather.

Получить свой `TELEGRAM_CHAT_ID` можно в Telegram у бота @userinfobot.

Узнать `PROJECT_ID`, `PROJECT_NUMBER` и `GOOGLE_APPLICATION_CREDENTIALS` от DialogFlow  можно в настройках своего аккаунта DialogFlow.

Для обучения бота у агента DialogFlow должны быть права доступа Администратор Dialogflow API. 


### Как запустить и использовать

1. Для запуска бота в Телеграме используйте команду: `python telegram_bot.py`

2. Для запуска бота в ВК используйте команду `python vk_bot.py`

3. Для обучения бота используйте команду `python df_API.py`. 
[Пример](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json) JSON-файла с обучающими фразами.

## Пример использования бота

[Телеграм-бот](https://t.me/dev_flower_shop_bot)
[ВК-бот](https://vk.com/im?sel=-224989418)
![Sample](https://s9.gifyu.com/images/SUs5O.gif)

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/)
# NotifierBot

Данный telegram-bot оповещает через телеграм об окончании проверки работы.

## Как работает?
Бот опрашивает через long poll сервер проверок работ devman, используя [API](https://dvmn.org/api/docs/).

## Используемые пакеты
`requests 2.31` - HTTP-методы.

`environs 9.5` - для переменных окружения из `.env`

`python-telegram-bot 13.14` - синхронная оболочка над телеграмовским ботом. 

## Переменные окружения
`PERSONAL_TOKEN` - персональный токен пользователя devman, который можно получить [здесь](https://dvmn.org/api/docs/). 

`BOT_TOKEN` - токен бота, который можно получить после создания бота через @BotFather в телеграме.

`CHAT_ID` - id-пользователя (ваш), которому бот будет присылать оповещения. Узнать свой `chat_id` можно через бота 
@userinfobot.

`LOGGING_DEBUG` - уровень логирования для отображения в консоли. True - уровень DEBUG, False - стандартный уровень 
logging.WARNING.

## Как запустить
- Создайте бота по [инструкции](https://github.com/python-telegram-bot/v13.x-wiki/wiki/Introduction-to-the-API).
- Cоздайте `.env` и заполните поля из раздела "Переменные окружения"
следующим образом `export PERSONAL_TOKEN=ваш_персональный_ключ` и так далее.
- Установите пакеты:
```shell
$ pip install -r requirements.txt
```
- Запустите бота из корня проекта:
```shell
$ python main.py
```
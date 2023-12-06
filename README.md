# NotifierBot

Данный telegram-bot оповещает через телеграм об окончании проверки работы.
Работает на **Python 3.10.12**.

## Как работает?
Бот опрашивает через long poll сервер проверок работ devman, используя [API](https://dvmn.org/api/docs/).

## Используемые пакеты
`requests 2.31` - HTTP-методы.

`environs 9.5` - для переменных окружения из `.env`

`python-telegram-bot 13.14` - синхронная оболочка над телеграмовским ботом. 

## Переменные окружения
`TELEGRAM_USER_TOKEN` - персональный токен пользователя devman, который можно получить [здесь](https://dvmn.org/api/docs/). 

`TELEGRAM_BOT_TOKEN` - токен бота, который можно получить после создания бота через @BotFather в телеграме.

`TELEGRAM_CHAT_ID` - id-пользователя (ваш), которому бот будет присылать оповещения. Узнать свой `chat_id` можно через бота 
@userinfobot.

`TELEGRAM_ERROR_BOT_TOKEN` - токен бота в который будет отправляться информация о запуске бота и его ошибках.

`LOGGING_DEBUG` - уровень логирования для отображения в консоли. True - уровень DEBUG, False - стандартный уровень 
logging.WARNING.

## <a name="howtolaunch" /> Как запускать?
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

## Как собрать образ и запустить контейнер с ботом?
- Прежде всего убедитесь, что у вас установлен [Docker](https://www.docker.com/get-started/).
- Создайте бота по инструкции, создайте и заполните `.env` из [Как запустить](#howtolaunch)
- Находясь в директории с Dockerfile, соберите образ через команду:
```shell
$ docker build -t review-bot-image .
```
- Запустите контейнер через команду:
```shell
$ docker run -d --name review-bot-container review-bot-image
```
- Для просмотра содержимого контейнера введите команду:
```shell
$ docker exec -it review-bot-container /bin/ash
```
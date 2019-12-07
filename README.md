# VK, Inst, FB Info

Бот для сбора информации по активным подписчикам в социальных сетях.


## Как установить

1. Клонировать GIT-репозиторий к себе.
2. `pip3 install -r requirements.txt`
3. Создать файл `.env` и положить в него следующие переменные:
    * `INST_LOGIN` - Ваш логин в инстаграм
    * `INST_PASSWORD` - Ваш пароль от инстаграм
    * `SERVICE_VK_TOKEN` - [Сервисный токен VK](https://vk.com/dev/access_token?f=3.%20%D0%A1%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BD%D1%8B%D0%B9%20%D0%BA%D0%BB%D1%8E%D1%87%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0)
    * `FB_ACCESS_TOKEN` - Токен Facebook

## Пример запуска

`python3 smm_analyze.py instagram`

Возможные ключи запуска:
* `instagram` - получить анализ Instagram
* `vk` - получить анализ VK
* `facebook` - получить анализ Facebook

Полную справку можно получить с помощью команды:

`python3 smm_analyze.py -h`


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org/modules)
# ВК и ТГ бот для тех. поддержки сервиса.

Боты снижают нагрузку на администраторов, отвечая на подготовленные заранее вопросы без участия человека.

Пример работы в ТГ:

![Untitled](https://github.com/user-attachments/assets/2c6a8218-641d-44fa-9496-eb52a3ac1732)

Пример работы в ВК:

![Untitled](https://github.com/user-attachments/assets/0b768ada-e949-4969-99af-1159178059f8)


### Как установить

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

Далее добавьте в папку с проектом файл `.env` и скопируйте туда следующий код:

```
VK_API_KEY=''
TG_TOKEN=''
DEV_TG_TOKEN=''
CHAT_ID=''
GOOGLE_APPLICATION_CREDENTIALS=''
```

`VK_API_KEY` - необходимо получить на сайте [Devman](https://vk.com/) во вкладке API в настройках созданной группы. 

`TG_TOKEN` - необходимо получить у FatherBot.

`DEV_TG_TOKEN` - необходимо получить у FatherBot. Токен для бота, который присылает уведомления об ошибках основных ботов.

`CHAT_ID` - id чата, чтобы узнать, необходимо написать боту `@userinfobot`. в телеграм.

`GOOGLE_APPLICATION_CREDENTIALS` - переменная окружения, где лежит путь до файла с ключами от Google, credentials.json. Подробнее читать [здесь](https://cloud.google.com/docs/authentication/api-keys).

### Как включить
Запуск скрипта осуществляется через консоль. 
Телеграм бот:
```
python tg_bot.py
```
ВКонтакте бот:
```
python vk_bot.py
```

Телеграм бот отвечает на каждое сообщение пользователя, а вк, только на те, на которые он обучен. Обучение ботов осуществляется.

### Обучение ботов

Обучение осуществляется через сервис [DialogFlow](https://dialogflow.cloud.google.com/#/login). Так же необходимо создать [агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent), которого нужно подключить к проекту DialogFlow Для автоматизации обучения используйте скрипт `dialog_flow_instruments`. Функция `create_api_key` используется для создания api ключа, а функция `create_intent` для обучения бота. Более подробное описание работы функций можно прочитать [здесь](https://cloud.google.com/dialogflow/es/docs/how/manage-intents#create_intent).

### Фича

Всю информацию об ошибках боты присылают в телеграм. Каждый бот можно запустить отдельно, они автономны.

### Цель проекта

Проект создан в образовательных целях.

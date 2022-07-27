# homework_bot
## Описание проекта homework_bot
Telegram-бот, будет обращаться к API сервиса Практикум.Домашка и узнавать статус домашней работы: взята ли домашняя работа в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

## Стек технологий
Python 3.7

requests

python-dotenv

python-telegram-bot

## Как запустить проект
### Шаг 1
Клонировать репозиторий с проектом себе на компьютер
```bash
git clone https://github.com/DumaDim/homework_bot.git
```

### Шаг 2
В созданной директории установите виртуальное окружение, активируйте его и установите необходимые зависимости
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Шаг 3
Создайте чат-бота Телеграм

### Шаг 4
Создайте в директории файл .env и поместите туда необходимые токены в формате 
```bash
PRAKTIKUM_TOKEN = 'ххххххххх'
TELEGRAM_TOKEN = 'ххххххххххх'
TELEGRAM_CHAT_ID = 'ххххххххххх'
```
### Шаг 5
Откройте файл homework.py и запустите код

### Пример ответа чат-бота
```bash
{
   "homeworks":[
      {
         "id":123,
         "status":"approved",
         "homework_name":"username__hw_python_oop.zip",
         "reviewer_comment":"Всё нравится",
         "date_updated":"2020-02-13T14:40:57Z",
         "lesson_name":"Итоговый проект"
      }
   ],
   "current_date":1581604970
}
```

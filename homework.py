from http import HTTPStatus
import os
import time
import logging
import telegram

import requests

from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Бот отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.info(f'Отправлено сообщение: "{message}"')
    except Exception as error:
        logging.error(f'Cбой отправки сообщения, ошибка: {error}')


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception:
        message = 'API ведет себя некорректно'
        logging.error(message)
        raise Exception(message)
    try:
        if response.status_code != HTTPStatus.OK:
            message = 'ЭНДПОИНТ не отвечает'
            logging.error(message)
            raise Exception(message)
    except Exception:
        message = 'API ведет себя некорректно'
        logging.error(message)
        raise Exception(message)
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    if not isinstance(response, dict):
        message = 'Ответ API не является словарем'
        raise TypeError(message)
    if not isinstance(response.get('homeworks'), list):
        raise TypeError("response['homeworks'] не является списком")
    if ['homeworks'][0] not in response:
        message = 'В ответе API нет данного ключа'
        raise IndexError(message)
    homework = response.get('homeworks')
    return homework


def parse_status(homework):
    """Инф-ция о статусе конкретной домашней работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if (homework_name or homework_status) is None:
        message = 'Ключа нет в ответе API'
        logging.error(message)
    if homework_status not in HOMEWORK_VERDICTS:
        message = 'Неизвестный статус домашней работы'
        raise KeyError(message)
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    if all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        return True
    return False


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0
    check_result = check_tokens()
    if check_result is False:
        message = 'Отсутствуют обязательные переменные окружения'
        logger.critical(message)
        raise SystemExit(message)

    while True:
        try:
            response = get_api_answer(current_timestamp)
            if 'current_date' in response:
                current_timestamp = response['current_date']
            homework = check_response(response)
            if homework is None:
                message = 'Отсутствует в ответе новый статус'
                logging.debug(message)
            elif homework is not None:
                message = parse_status((homework)[0])
                if message is not None:
                    send_message(bot, message)
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        level=logging.INFO,
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    logger = logging.getLogger(__name__)
    main()

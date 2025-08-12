import requests
from ..config import config
from loguru import logger


def get_token() -> str:
    url = f"http://{config.api_url}/api/login"
    payload = {
        "username": config.login.get_secret_value(),
        "password": config.password.get_secret_value()
    }
    logger.debug(f"Попытка логина на {url} с пользователем {payload['username']}")
    try:
        resp = requests.post(url, json=payload)
        logger.debug(f"Получен ответ от сервера: статус {resp.status_code}")
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса при логине: {e}")
        raise
    
    try:
        data = resp.json()
    except Exception as e:
        logger.error(f"Ошибка парсинга JSON из ответа: {e}")
        raise

    token = data.get("data", {}).get("token")
    if token:
        logger.success("Токен успешно получен")
    else:
        logger.warning("Токен в ответе отсутствует")
    return token

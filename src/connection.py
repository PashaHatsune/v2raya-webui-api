import uuid
import requests
from loguru import logger

from config import config
from src.login import get_token


def connect_server(server_id, sub_index=0, outbound="proxy"):
    url = f"http://{config.api_url}/api/connection"
    data = {
        "id": server_id,
        "_type": "subscriptionServer",
        "sub": sub_index,
        "outbound": outbound
    }
    headers = {
        "Authorization": get_token(),
        "Content-Type": "application/json",
        "X-V2raya-Request-Id": str(uuid.uuid4()),
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Origin": f"http://{config.api_url}",
        "Referer": f"http://{config.api_url}",
        "Connection": "keep-alive"
    }

    logger.debug(f"Запрос подключения к серверу {server_id} с данными: {data}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info(f"Подключение успешно, статус: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"Ошибка подключения к серверу {server_id}: {e}")
        return f"ERROR: {e}"

    try:
        resp_json = response.json()
        code = resp_json.get("code")
        running = resp_json.get("data", {}).get("running")
        logger.debug(f"Ответ сервера: code={code}, running={running}")
    except Exception as e:
        logger.error(f"Не удалось распарсить JSON ответ: {e}")
        logger.debug(f"Ответ сервера (raw): {response.text}")

    on_status = on_v2raya()
    logger.debug(f"Статус v2raya после подключения: code={on_status.get('code') if on_status else None}, running={on_status.get('data', {}).get('running') if on_status else None}")

    return "SUCCESS"


def off_v2raya():
    url = f"http://{config.api_url}/api/v2ray"
    headers = {
        "Host": f"{config.api_url}",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": f"http://{config.api_url}",
        "Authorization": get_token(),
        "X-V2raya-Request-Id": str(uuid.uuid4()),
        "Origin": f"http://{config.api_url}",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Priority": "u=0",
        "Content-Length": "0"
    }
    logger.debug("Отправка запроса выключения v2raya")
    try:
        response = requests.post(url, headers=headers, data=b"")
        response.raise_for_status()
        try:
            data = response.json()
            logger.info(f"v2raya выключен, code={data.get('code')}, running={data.get('data', {}).get('running')}")
            return data
        except Exception:
            logger.info(f"v2raya выключен, но не удалось распарсить JSON, raw: {response.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Ошибка при выключении v2raya: {e}")
        return None


def on_v2raya():
    url = f"http://{config.api_url}/api/v2ray"
    headers = {
        "Host": f"{config.api_url}",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": f"http://{config.api_url}",
        "Authorization": get_token(),
        "X-V2raya-Request-Id": str(uuid.uuid4()),
        "Origin": f"http://{config.api_url}",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Priority": "u=0",
        "Content-Length": "0"
    }
    logger.debug("Отправка запроса включения v2raya")
    try:
        response = requests.post(url, headers=headers, data=b"")
        response.raise_for_status()
        try:
            data = response.json()
            logger.info(f"v2raya включен, code={data.get('code')}, running={data.get('data', {}).get('running')}")
            return data
        except Exception:
            logger.info(f"v2raya включен, но не удалось распарсить JSON, raw: {response.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Ошибка при включении v2raya: {e}")
        return None
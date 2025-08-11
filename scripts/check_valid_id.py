import requests
from loguru import logger
from config import config  # если надо взять API_URL из конфига





def get_touch_data():
    try:
        logger.debug(f"Отправляем GET запрос на /api/touch")
        resp = requests.get(
            url=f"http://{config.api_url}/api/touch",
            headers={
                "Host": "192.168.1.1:2019",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Referer": "http://192.168.1.1:2019/",
                "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTc1MjUwMzQsInVuYW1lIjoibWlrdSJ9.MWhqbSbQ4CdOrhrpifSYfDWaND0yJ4yjhRpIjNIGj8A",
                "X-V2raya-Request-Id": "static-or-dynamic-id-if-needed",
                "Origin": "http://192.168.1.1:2019",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Priority": "u=0"
            },
            timeout=5
        )

        resp.raise_for_status()
        data = resp.json()
        logger.info(f"v2raya: code={data.get('code')}, running={data.get('data', {}).get('running')}")

        if data.get("code") != "SUCCESS":
            logger.error(f"API вернул ошибку: {data.get('message')}")
            return None

        return data.get("data", {})

    except Exception as e:
        logger.error(f"Ошибка запроса: {e}")
        return None


def get_connected_server_id(touch_data):
    connected = touch_data.get("touch", {}).get("connectedServer", [])
    if not connected:
        logger.warning("Нет подключённого сервера")
        return None

    server_id = connected[0].get("id")
    logger.info(f"Подключённый сервер ID: {server_id}")
    return server_id


def get_all_servers(touch_data):
    subscriptions = touch_data.get("touch", {}).get("subscriptions", [])
    servers = [srv for sub in subscriptions for srv in sub.get("servers", [])]
    logger.info(f"Всего серверов в подписках: {len(servers)}")
    return servers


def check_server_valid(server_id, servers):
    for srv in servers:
        if srv.get("id") == server_id:
            logger.success(f"Сервер с ID {server_id} валиден и найден: {srv.get('name', 'без имени')}")
            return True

    logger.warning(f"Сервер с ID {server_id} НЕ найден среди подписок")
    return False


if __name__ == "__main__":
    touch_data = get_touch_data()
    if not touch_data:
        exit(1)

    connected_id = get_connected_server_id(touch_data)
    if connected_id is None:
        exit(1)

    all_servers = get_all_servers(touch_data)
    check_server_valid(connected_id, all_servers)

# import requests
# from loguru import logger

# from src.utils import HEADERS

# API_URL = "http://192.168.1.1:2019/api/touch"

# def get_touch_data():
#     try:
#         resp = requests.get(API_URL, headers=HEADERS, timeout=5)
#         resp.raise_for_status()
#         data = resp.json()
#         print(data)
#         if data.get("code") != "SUCCESS":
#             logger.error(f"API вернул ошибку: {data.get('message')}")
#             return None
#         return data.get("data", {})
#     except Exception as e:
#         logger.error(f"Ошибка запроса к {API_URL}: {e}")
#         return None

# def get_connected_server_id(touch_data):
#     connected = touch_data.get("touch", {}).get("connectedServer", [])
#     if not connected:
#         logger.warning("Нет подключённого сервера")
#         return None
#     server = connected[0]
#     server_id = server.get("id")
#     logger.info(f"Подключённый сервер ID: {server_id}")
#     return server_id

# def get_all_servers(touch_data):
#     # Считаем, что серверы лежат в subscriptions -> servers
#     servers = []
#     subscriptions = touch_data.get("touch", {}).get("subscriptions", [])
#     for sub in subscriptions:
#         servers.extend(sub.get("servers", []))
#     logger.info(f"Всего серверов в подписках: {len(servers)}")
#     return servers

# def check_server_valid(server_id, servers):
#     for srv in servers:
#         if srv.get("id") == server_id:
#             logger.success(f"Сервер с ID {server_id} валиден и найден: {srv.get('name', 'без имени')}")
#             return True
#     logger.warning(f"Сервер с ID {server_id} НЕ найден среди подписок")
#     return False

# if __name__ == "__main__":
#     touch_data = get_touch_data()
#     if not touch_data:
#         exit(1)

#     connected_id = get_connected_server_id(touch_data)
#     if connected_id is None:
#         exit(1)

#     all_servers = get_all_servers(touch_data)
#     check_server_valid(connected_id, all_servers)

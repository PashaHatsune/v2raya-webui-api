import requests
import urllib.parse
import uuid
import json
from config import config
from src.get_subscriptions import get_subscriptions
from src.login import get_token
from loguru import logger


def ping_server(server) -> dict:
    whiches = [{
        "id": server["id"],
        "_type": server["_type"],
        "sub": server.get("sub_index", 0)
    }]
    param = urllib.parse.quote(json.dumps(whiches))
    url = f"http://{config.api_url}/api/httpLatency?whiches={param}"

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

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        logger.info(
            f"Пингуем {server['name']}, CODE: {data['code']} | "
            f"ID: {data['data']['whiches'][0]['id']} | "
            f"MS: {data['data']['whiches'][0]['pingLatency']}"
        )
        return data
    except Exception as e:
        logger.error(f"Ошибка при пинге сервера {server['name']}: {e}")
        return {}


def ping_all_servers(servers: list[dict] | None = None) -> list[tuple[dict, dict]]:
    if not servers:
        servers = get_subscriptions()

    whiches = [{
        "id": srv["id"],
        "_type": srv["_type"],
        "sub": srv.get("sub_index", 0)
    } for srv in servers]

    param = urllib.parse.quote(json.dumps(whiches))
    

    try:
        response = requests.get(
            url=f"http://{config.api_url}/api/httpLatency?whiches={param}",
            headers={
                "Authorization": get_token(),
                "Content-Type": "application/json",
                "X-V2raya-Request-Id": str(uuid.uuid4()),
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, text/plain, */*",
                "Origin": f"http://{config.api_url}",
                "Referer": f"http://{config.api_url}",
                "Connection": "keep-alive"
            }
        )
        response.raise_for_status()
        data = response.json()

        results = []
        good_servers = []

        if data.get("code") == "SUCCESS":
            whiches_data = data["data"]["whiches"]
            for which in whiches_data:
                srv_id = which.get("id")
                latency_str = which.get("pingLatency", "").replace("ms", "").strip()
                srv = next((s for s in servers if s["id"] == srv_id), None)
                if srv:
                    results.append((srv, which))
                    if latency_str.isdigit():
                        latency = int(latency_str)
                        if latency < 400:
                            good_servers.append({
                                "name": srv["name"],
                                "id": srv["id"],
                                "latency_ms": latency
                            })

            with open("good_servers.json", "w", encoding="utf-8") as f:
                json.dump(good_servers, f, indent=4, ensure_ascii=False)
            logger.info(f"Сохранил {len(good_servers)} валидных серверов в good_servers.json")
        else:
            logger.error(f"Ошибка в ответе на пинг: {data.get('message', 'без сообщения')}")

        return results

    except Exception as e:
        logger.error(f"Ошибка пинга серверов: {e}")
        return []

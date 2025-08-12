import uuid

import requests
from loguru import logger

from ..config import config
from .login import get_token
from .utils import json_data


def get_subscriptions() -> list[dict]:

    response = requests.put(
        url=f"http://{config.api_url}/api/subscription",
        headers={
            "Authorization": get_token(),
            "Content-Type": "application/json",
            "X-V2raya-Request-Id": str(uuid.uuid4()),
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": f"http://{config.api_url}",
            "Referer": f"http://{config.api_url}",
            "Connection": "keep-alive"
        },
        json=json_data
    )
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Ошибка запроса подписок: {e}")
        logger.error(response.text)
        return []

    subs = response.json()
    if subs.get("code") == "SUCCESS" and "data" in subs:
        touch = subs["data"].get("touch", {})
        subscriptions = touch.get("subscriptions", [])
        servers = []
        for i, sub in enumerate(subscriptions):
            for srv in sub.get("servers", []):
                net = str(srv.get("net", "")).lower()
                if any(x in net for x in ["xhttp", "httpupgrade+tls", "httpupgrade"]):
                    continue

                # Добавлять sub_index один раз достаточно
                srv["sub_index"] = i

                is_valid = "s" in net or "ss" in net
                if is_valid:
                    servers.append(srv)
                    logger.debug(f"Добавляем сервер: {srv.get('name')} | Net: {net}")
                else:
                    logger.debug(
                        f"Игнорируем сервер {srv.get('name')} | "
                        f"Net: {net or 'не указан'}, "
                        f"Адрес: {srv.get('address', 'не указан')}"
                    )

        count = len(servers)
        logger.info(f"Всего серверов в подписках: {count}")
        return servers
    else:
        logger.error(f"Ошибка получения подписок: {subs.get('message', 'неизвестная ошибка')}")
        return []

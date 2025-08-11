import requests

from config import config


def get_token() -> str:
    resp = requests.post(f"http://{config.api_url}/api/login", json={
        "username": config.login.get_secret_value(),
        "password": config.password.get_secret_value()
    })

    resp.raise_for_status()
    data = resp.json()

    tokn = data.get("data", {}).get("token")
    return tokn

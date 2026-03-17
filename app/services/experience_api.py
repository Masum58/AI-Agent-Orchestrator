import requests
from app.core.logger import logger

BASE_URL = "http://172.252.13.97:8004/api"


def get_experience(user_id: str):
    try:
        res = requests.get(
            f"{BASE_URL}/experience/user/{user_id}",
            timeout=3
        )

        res.raise_for_status()

        data = res.json()

        # Handle both formats (list or wrapped)
        if isinstance(data, list):
            return data

        return data.get("data", [])

    except Exception as e:
        logger.error(f"Experience fetch failed: {str(e)}")
        return []
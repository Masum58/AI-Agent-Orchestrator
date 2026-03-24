import requests
from app.core.logger import logger

BASE_URL = "https://test21.fireai.agency"


# -------------------------------------------------
# SEARCH EXPERIENCE (Long-term memory)
# -------------------------------------------------
def search_experience(user_id: str, query: str):
    """
    Fetch experience from API and return clean list
    """

    url = f"{BASE_URL}/api/experience/user/for-ai/{user_id}"

    try:
        logger.info(f"[EXPERIENCE API] Fetching for user_id={user_id}")

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        json_resp = response.json()

        # 🔥 FIX: correct extraction
        data_block = json_resp.get("data", {})
        experience_list = data_block.get("data", [])

        logger.info(f"[EXPERIENCE API] Retrieved {len(experience_list)} records")

        return experience_list

    except Exception as e:
        logger.error(f"[EXPERIENCE API ERROR] {str(e)}", exc_info=True)
        return []


# -------------------------------------------------
# SAVE EXPERIENCE (Long-term memory write)
# -------------------------------------------------
def save_experience(user_id: str, role: str, content: str):
    try:
        payload = {
            "actor": role.lower(),        # user / agent
            "event_type": "message",
            "content": content,
            "user_id": user_id
        }

        res = requests.post(
            f"{BASE_URL}/experience",
            json=payload,
            timeout=3
        )

        logger.info(f"Experience saved: {res.status_code}")

    except Exception as e:
        logger.error(f"Experience save failed: {str(e)}")
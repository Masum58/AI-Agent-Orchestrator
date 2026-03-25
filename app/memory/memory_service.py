from typing import List, Dict
from app.core.logger import logger

# 🔥 USE EXPERIENCE API (temporary fix)
from app.services.experience_api import search_experience


# -------------------------------------------------
# Function: get_instance_messages
# -------------------------------------------------
def get_instance_messages(user_id: str) -> List[Dict]:
    """
    Fetch conversation history and normalize for LLM
    """

    try:
        # -----------------------------
        # 1. Fetch from EXPERIENCE API
        # -----------------------------
        messages = search_experience(user_id, query="")

        logger.info(f"[MEMORY] Raw experience count: {len(messages)}")

        if not messages:
            return []

        # -----------------------------
        # 2. Normalize messages
        # -----------------------------
        normalized_messages = []

        for instance in messages:
            if not isinstance(instance, dict):
                continue

            user_msg = instance.get("userQuery")
            ai_msg = instance.get("aiResponse")

            # User message
            if user_msg:
                normalized_messages.append({
                    "role": "user",
                    "content": str(user_msg).strip()
                })

            # Assistant message
            if ai_msg:
                normalized_messages.append({
                    "role": "assistant",
                    "content": str(ai_msg).strip()
                })

        logger.info(f"[MEMORY] Normalized messages: {len(normalized_messages)}")

        return normalized_messages

    except Exception as e:
        logger.error(f"[Memory Service Error] get_instance_messages: {e}")
        return []


# -------------------------------------------------
# Function: search_experience (KEEP for fallback)
# -------------------------------------------------
def search_experience_local(query: str) -> List[str]:
    """
    Local fallback (not used now)
    """
    return [
        "User previously asked about contract review",
        "Agent generated NDA summary"
    ]
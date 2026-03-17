from typing import List, Dict


def format_conversation(messages: List[Dict]) -> List[Dict]:
    """
    Convert DB messages to LLM-compatible format
    """

    # Allowed roles for LLM
    allowed_roles = ["user", "assistant", "system"]

    formatted = []

    for msg in messages:

        # Get role and normalize
        role = msg.get("role", "").lower()

        # If role is not valid → default to user
        if role not in allowed_roles:
            role = "user"

        # Clean content
        content = msg.get("content", "").strip()

        # Skip empty messages
        if not content:
            continue

        formatted.append({
            "role": role,
            "content": content
        })

    return formatted
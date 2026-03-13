# This file is responsible for retrieving memory data
# Later this will call database APIs

from typing import List, Dict


# Get conversation history for the current instance
def get_instance_messages(instance_id: str) -> List[Dict]:

    # TEMP MOCK DATA
    # This will later be replaced by a database API call
    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello, how can I assist you?"}
    ]


# Get past experience logs
def search_experience(query: str) -> List[str]:

    # TEMP MOCK DATA
    return [
        "User previously asked about contract review",
        "Agent generated NDA summary"
    ]
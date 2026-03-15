# This file is responsible for retrieving memory data
# Now it connects to the real database APIs
from app.services.database_client import get_user_messages 
from typing import List, Dict
import requests

# Database service base URL
BASE_URL = "http://172.252.13.97:8004"


# Get conversation history for the current instance
def get_instance_messages(user_id: str) -> List[Dict]:

    url = f"{BASE_URL}/api/admin/user-instances/for-ai/{user_id}"

    response = requests.get(url)

    data = response.json()

    # Return only the message list
    return data.get("data", [])


# Get past experience logs (currently not provided by database yet)
# Keep mock for now until the API is ready
def search_experience(query: str) -> List[str]:

    # Temporary fallback data
    return [
        "User previously asked about contract review",
        "Agent generated NDA summary"
    ]
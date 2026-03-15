# Import the requests library
# This library allows our system to send HTTP requests to the database service.
import requests


# Base URL of the database service
BASE_URL = "http://172.252.13.97:8004"


# -------------------------------------------------
# Function: get_agents
# -------------------------------------------------
# This function retrieves all AI agent configurations
# such as identity and behaviour from the database.
def get_agents():

    # Build the API URL
    url = f"{BASE_URL}/api/agen-management/all/for-ai"

    # Send a GET request to the database service
    response = requests.get(url)

    # Convert response to JSON
    data = response.json()

    # Return only the useful data section
    return data.get("data", [])


# -------------------------------------------------
# Function: get_users
# -------------------------------------------------
# This function retrieves all mobile users from the database.
def get_users():

    url = f"{BASE_URL}/api/admin/mobile-users/for-ai"

    response = requests.get(url)

    data = response.json()

    return data.get("data", [])


# -------------------------------------------------
# Function: get_user_messages
# -------------------------------------------------
# This function loads conversation history
# for a specific user.
def get_user_messages(user_id: str):

    url = f"{BASE_URL}/api/admin/user-instances/for-ai/{user_id}"

    response = requests.get(url)

    data = response.json()

    return data.get("data", [])
# Import the requests library
# This library helps our system send HTTP requests to other services.
# In this case, we will talk to the database service API.
import requests


# Base URL of the database service
# All API calls will start with this base address.
BASE_URL = "http://database-service"


# -------------------------------------------------
# Function: get_agent
# -------------------------------------------------
# This function requests the configuration of an AI agent
# from the database service.
# Example: identity, behaviour, etc.
def get_agent(agent_id: str):

    # Build the full API URL
    # Example result: http://database-service/agents/123
    url = f"{BASE_URL}/agents/{agent_id}"

    # Send a GET request to the database service
    # The database will return the agent configuration.
    response = requests.get(url)

    # Convert the response into JSON format
    # and return the data to the caller.
    return response.json()


# -------------------------------------------------
# Function: get_instance_messages
# -------------------------------------------------
# This function loads conversation history
# for a specific chat session (instance).
# It helps the AI understand previous messages.
def get_instance_messages(instance_id: str):

    # Build the API URL
    # Example result:
    # http://database-service/instances/demo-instance/messages
    url = f"{BASE_URL}/instances/{instance_id}/messages"

    # Send a GET request to the database service
    response = requests.get(url)

    # Return the conversation messages as JSON
    return response.json()
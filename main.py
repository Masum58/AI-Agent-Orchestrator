# Import FastAPI framework
# FastAPI is used to create web APIs so other systems or users can send requests to our AI service.
from fastapi import FastAPI, Query

# Import datetime to add timestamps to responses
# This helps track when the AI response was generated.
from datetime import datetime

# Import uuid to generate unique conversation IDs
# This ensures each chat session can be tracked separately.
import uuid

# Import the AI orchestrator
# The orchestrator controls the full AI workflow and coordinates all AI components.
from app.orchestrator.agent_runner import run_agent


# Create the FastAPI application
# This represents our AI service backend.
app = FastAPI()


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------
# This endpoint is used to check if the API service is running.
# When someone visits the root URL, this message confirms the system is active.
@app.get("/")
def root():
    return {"message": "AI Agent Service Running"}


# --------------------------------------------------
# AI Chat Endpoint
# --------------------------------------------------
# This endpoint receives a user message and sends it to the AI agent.
# The AI agent processes the message and returns a generated response.
@app.post(
    "/chat",
    summary="AI Chat Endpoint",
    description="""
This endpoint sends a user message to the AI agent and returns an AI-generated response.

Full AI Pipeline:
1. Load agent configuration
2. Load conversation history
3. Search experience logs
4. Build structured prompt
5. Send prompt to LLM
6. Return generated response
"""
)
def chat(

    # user_query is the message from the user
    # It is required and represents what the user wants to ask the AI.
    user_query: str = Query(
        ...,
        description="The message or question that the user wants to ask the AI agent.",
        example="Explain what a contract is"
    ),

    # conversation_id is used to identify a chat session
    # If it is not provided, the system will create a new conversation.
    conversation_id: str = Query(
        None,
        description="Unique conversation session id. If not provided, a new conversation will be created."
    )
):

    # --------------------------------------------------
    # Generate Conversation ID
    # --------------------------------------------------
    # If no conversation ID is provided, create a new one.
    # This helps track each conversation separately.
    if not conversation_id:
        conversation_id = f"conv_{uuid.uuid4().hex[:10]}"

    # --------------------------------------------------
    # Run the AI Orchestrator
    # --------------------------------------------------
    # The orchestrator manages the full AI pipeline.
    # It collects context, builds the prompt, sends it to the AI model,
    # and returns the generated response.
    result = run_agent(user_query)

    # Extract the AI response content
    ai_response = result["content"]

    # Extract memory information used during the response generation
    memory_info = result["memory"]

    # --------------------------------------------------
    # Token Usage (Placeholder)
    # --------------------------------------------------
    # These values will track token usage for the AI model.
    # This helps measure cost and performance in production systems.
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0

    # --------------------------------------------------
    # Return API Response
    # --------------------------------------------------
    # The API returns a structured JSON response containing
    # the conversation ID, user message, AI response, memory data,
    # token usage, and timestamp.
    return {
        "success": True,
        "message": "AI response generated successfully",
        "data": {
            "conversation_id": conversation_id,
            "role": "assistant",
            "user_query": user_query,
            "content": ai_response,
            "agent": {
                "agent_name": "Sales_agent"
            },
            "memory": memory_info,
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    }
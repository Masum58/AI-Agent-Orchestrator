# Import FastAPI framework
# FastAPI is used to create web APIs so other systems or users can talk to our service
from fastapi import FastAPI, Query

# Import the function that sends prompts directly to the AI model
from app.llm.openai_adapter import generate_response

# Import the AI orchestrator (main AI workflow controller)
from app.orchestrator.agent_runner import run_agent


# Create a FastAPI application instance
# This represents our AI service
app = FastAPI()


# Root endpoint to confirm the API service is running
@app.get("/")
def root():

    return {"message": "AI Agent Service Running"}


# Test endpoint to verify the OpenAI connection works
@app.get(
    "/test-ai",
    summary="Test AI response",
    description="This endpoint sends a simple test prompt to the AI model to verify that the LLM integration is working correctly."
)
def test_ai():

    # Send a simple test prompt to the AI model
    reply = generate_response("Say hello in one sentence")

    # Return the AI response
    return {"ai_response": reply}


# Production AI chat endpoint
@app.post(
    "/chat",
    summary="AI Chat Endpoint",
    description="""
This endpoint sends a user message to the AI agent and returns an AI-generated response.

The request goes through the full AI pipeline:
1. Retrieve conversation history
2. Retrieve past experience logs
3. Build a structured prompt
4. Send the prompt to the LLM
5. Return the generated response
"""
)
def chat(
    user_query: str = Query(
        ...,
        description="The message or question that the user wants to ask the AI agent. Example: 'Explain what a contract is.'"
    )
):

    response = run_agent(user_query)

    return {"response": response}
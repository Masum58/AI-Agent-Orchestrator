# This file works as the main AI controller (orchestrator).
# It manages the whole AI pipeline step by step.
# The orchestrator decides what data to collect and how to talk to the AI model.

from app.context.prompt_builder import build_prompt
from app.llm.openai_adapter import generate_response
from app.memory.memory_service import get_instance_messages, search_experience


# -------------------------------------------------
# Function: run_agent
# -------------------------------------------------
# This function is the main entry point of the AI agent.
# It receives the user's question and returns the AI's answer.
def run_agent(user_query: str):

    # -------------------------------------------------
    # 1. Agent Configuration
    # -------------------------------------------------
    # Here we define the identity and behaviour of the AI.
    # In the future this information will likely come from a database.
    # For now we define it directly in the code.
    identity = "You are a helpful AI assistant."
    behaviour = "Be clear, concise, and professional."

    # -------------------------------------------------
    # 2. Get Conversation History
    # -------------------------------------------------
    # The system loads previous messages from memory.
    # This helps the AI understand what was discussed before.
    # "demo-instance" represents the current chat session.
    conversation = get_instance_messages("demo-instance")

    # -------------------------------------------------
    # 3. Search Past Experiences
    # -------------------------------------------------
    # The system searches stored experiences that may be
    # related to the current user question.
    # These experiences help the AI give better answers.
    experience = search_experience(user_query)

    # -------------------------------------------------
    # 4. Build the Prompt
    # -------------------------------------------------
    # We combine all important information into a single prompt.
    # This prompt will include:
    # - Agent identity
    # - Behaviour rules
    # - Past experiences
    # - Conversation history
    # - Current user question
    prompt = build_prompt(
        identity=identity,
        behaviour=behaviour,
        experience=experience,
        conversation=conversation,
        user_query=user_query
    )

    # -------------------------------------------------
    # 5. Send the Prompt to the AI Model
    # -------------------------------------------------
    # The prompt is sent to the AI model through the LLM adapter.
    # The AI model reads the prompt and generates a response.
    response = generate_response(prompt)

    # Return the final AI answer
    return response
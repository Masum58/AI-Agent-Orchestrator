# This file works as the main AI controller (orchestrator).
# It manages the full AI workflow step by step.

# Import the function that builds the final prompt for the AI model
from app.context.prompt_builder import build_prompt

# Import the system logger to record important events
from app.core.logger import logger

# Import the function that sends prompts to the AI model
from app.llm.openai_adapter import generate_response

# Import memory functions
# These functions load past conversations and experiences
from app.memory.memory_service import get_instance_messages, search_experience


# -------------------------------------------------
# Function: run_agent
# -------------------------------------------------
# This function runs the full AI agent pipeline.
# It receives a user question and returns an AI-generated answer.
def run_agent(user_query: str, user_id: str = "demo-user"):

    # Record that the AI pipeline has started
    logger.info("Starting AI agent pipeline")

    # -------------------------------------------------
    # 1. Agent Configuration
    # -------------------------------------------------
    # These define the role and behavior of the AI agent.
    # In the future this data will be loaded from a database.
    identity = "You are a helpful AI assistant."
    behaviour = "Be clear, concise, and professional."

    # -------------------------------------------------
    # 2. Load Conversation History (Short-term memory)
    # -------------------------------------------------
    # The system loads recent messages from the conversation.
    # This helps the AI understand what was previously discussed.
    conversation = get_instance_messages(user_id)

    # Track whether short-term memory was used
    short_term_memory_used = True if conversation else False

    # -------------------------------------------------
    # 3. Search Past Experiences (Long-term memory)
    # -------------------------------------------------
    # The system searches stored experiences related to the question.
    # These experiences can help the AI generate better answers.
    experience = search_experience(user_query)

    # Track whether long-term memory was used
    long_term_memory_used = True if experience else False

    # -------------------------------------------------
    # 4. Build Prompt
    # -------------------------------------------------
    # Combine all information into a structured prompt.
    # The prompt includes:
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

    # Log that the prompt was successfully created
    logger.info("Prompt successfully built")

    # Print the prompt for debugging
    # This helps developers see exactly what the AI receives.
    # This line is usually removed in production systems.
    print(prompt)

    # -------------------------------------------------
    # 5. Call the AI Model
    # -------------------------------------------------
    # Send the prompt to the AI model and receive a response.
    response = generate_response(prompt)

    # Record that the AI has generated a response
    logger.info("AI response generated")

    # -------------------------------------------------
    # Return structured result
    # -------------------------------------------------
    # The API layer will use this result to create the final API response.
    return {
        "content": response,
        "memory": {
            "short_term_used": short_term_memory_used,
            "long_term_used": long_term_memory_used
        }
    }
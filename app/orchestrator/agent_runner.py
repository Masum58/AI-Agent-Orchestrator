# Orchestrator: Main AI controller

from app.context.prompt_builder import build_prompt
from app.core.logger import logger
from app.llm.openai_adapter import generate_response

# DB integrations
from app.services.experience_api import get_experience
from app.utils.conversation_formatter import format_conversation


def run_agent(user_query: str, user_id: str = "demo-user") -> dict:
    """
    Runs the full AI pipeline and returns structured output
    """

    try:
        logger.info("Starting AI agent pipeline")

        # -----------------------------
        # 1. Agent Config
        # -----------------------------
        identity = "You are a helpful AI assistant."
        behaviour = "Be clear, concise, and professional."

        # -----------------------------
        # 2. Short-term Memory (FROM DB - EXPERIENCE API)
        # -----------------------------
        raw_conversation = []

        try:
            raw_conversation = get_experience(user_id)

            if not isinstance(raw_conversation, list):
                logger.warning("Invalid experience format from DB")
                raw_conversation = []

        except Exception as e:
            logger.error(f"Experience fetch failed: {str(e)}")
            raw_conversation = []

        # -----------------------------
        # Format conversation for LLM
        # -----------------------------
        try:
            conversation = format_conversation(raw_conversation)
        except Exception as e:
            logger.error(f"Conversation formatting failed: {str(e)}")
            conversation = []

        # Limit memory (VERY IMPORTANT for token control)
        conversation = conversation[-5:]

        short_term_memory_used = bool(conversation)

        logger.info(f"Loaded {len(conversation)} conversation messages")

        # -----------------------------
        # 3. Long-term Memory (placeholder)
        # -----------------------------
        # TODO: replace with semantic search API later
        experience = []
        long_term_memory_used = False

        # -----------------------------
        # 4. Build Prompt
        # -----------------------------
        prompt = build_prompt(
            identity=identity,
            behaviour=behaviour,
            experience=experience,
            conversation=conversation,
            user_query=user_query
        )

        logger.info("Prompt successfully built")
        logger.debug(f"Prompt preview: {prompt[:300]}")

        # -----------------------------
        # 5. Call LLM
        # -----------------------------
        llm_response = generate_response(prompt)

        logger.info("AI response generated")

        # -----------------------------
        # 6. Output cleaning
        # -----------------------------
        reply = ""

        if isinstance(llm_response, dict):
            reply = (llm_response.get("content") or "").strip()
        elif isinstance(llm_response, str):
            reply = llm_response.strip()

        if not reply:
            reply = "I'm not sure how to respond to that."

        # -----------------------------
        # Return Structured Response
        # -----------------------------
        return {
            "reply": reply,
            "usage": llm_response.get("usage", {}) if isinstance(llm_response, dict) else {},
            "model": llm_response.get("model", "unknown") if isinstance(llm_response, dict) else "unknown",
            "memory": {
                "short_term_used": short_term_memory_used,
                "long_term_used": long_term_memory_used
            }
        }

    except Exception as e:
        logger.error(f"Agent pipeline failed: {str(e)}", exc_info=True)

        return {
            "reply": "Sorry, something went wrong while processing your request.",
            "usage": {},
            "model": "unknown",
            "memory": {
                "short_term_used": False,
                "long_term_used": False
            },
            "error": True
        }
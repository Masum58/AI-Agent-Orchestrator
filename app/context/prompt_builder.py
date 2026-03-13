from typing import List, Dict


def build_prompt(
    identity: str,
    behaviour: str,
    experience: List[str],
    conversation: List[Dict],
    user_query: str
) -> str:
    
    # This list will store different parts of the prompt.
    # Later we will combine all parts into one final text.
    sections = []

    # -----------------------------
    # 1. Agent Identity
    # -----------------------------
    # Here we tell the AI who it is.
    # Example: "You are a helpful customer support assistant"
    sections.append("### AGENT IDENTITY")
    sections.append(identity)

    # -----------------------------
    # 2. Behaviour Rules
    # -----------------------------
    # Here we define how the AI should behave.
    # Example: polite, short answers, professional tone.
    sections.append("\n### BEHAVIOUR")
    sections.append(behaviour)

    # -----------------------------
    # 3. Past Experience
    # -----------------------------
    # Sometimes the AI can learn from previous experiences.
    # If there are any stored experiences, we include them here.
    # This helps the AI make better decisions.
    if experience:
        sections.append("\n### PAST EXPERIENCE")

        # Each experience is added as a bullet point.
        for exp in experience:
            sections.append(f"- {exp}")

    # -----------------------------
    # 4. Recent Conversation
    # -----------------------------
    # To help the AI understand context,
    # we include recent messages from the conversation.
    # Each message has two parts:
    # role (user or assistant)
    # content (what was said)
    if conversation:
        sections.append("\n### RECENT CONVERSATION")

        for msg in conversation:
            role = msg.get("role")
            content = msg.get("content")

            # Example format:
            # USER: Hello
            # ASSISTANT: Hi, how can I help?
            sections.append(f"{role.upper()}: {content}")

    # -----------------------------
    # 5. User Question
    # -----------------------------
    # This is the new question the user just asked.
    # The AI must answer this question.
    sections.append("\n### USER QUESTION")
    sections.append(user_query)

    # -----------------------------
    # 6. Response Section
    # -----------------------------
    # This tells the AI where it should write the answer.
    sections.append("\n### RESPONSE")

    # -----------------------------
    # Final Step
    # -----------------------------
    # Join all sections into one single text prompt.
    # Each part will be separated by a new line.
    return "\n".join(sections)
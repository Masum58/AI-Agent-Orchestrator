from typing import List, Dict


def build_prompt(
    identity: str,
    behaviour: str,
    experience: List[str],
    conversation: List[Dict],
    user_query: str
) -> str:
    
    # This list will store different parts of the prompt.
    
    sections = []

    # -----------------------------
    # 1. Agent Identity
    # -----------------------------
    # Here we tell the AI who it is.
    # Example: "You are a helpful customer support assistant"
    sections.append("### AGENT IDENTITY")
    sections.append(identity.strip())

    # -----------------------------
    # 2. Behaviour Rules
    # -----------------------------
    # Here we define how the AI should behave.
    # Example: polite, short answers, professional tone.
    sections.append("\n### BEHAVIOUR")
    sections.append(behaviour.strip())

    # -----------------------------
    # 3. Past Experience
    # -----------------------------
    # Sometimes the AI can learn from previous experiences.
    # If there are any stored experiences, we include them here.
    # This helps the AI make better decisions.

    sections.append("\n### EXPERIENCE MEMORY")
    if experience:
        

        # Each experience is added as a bullet point.
        for exp in experience:
            if exp:
                sections.append(f"- {exp}")
            else:
                sections.append("No relevant experience found.")

    # -----------------------------
    # 4. Recent Conversation
    sections.append("\n### RECENT CONVERSATION")
    # -----------------------------
    # To help the AI understand context,
    # we include recent messages from the conversation.
    # Each message has two parts:
    # role (user or assistant)
    # content (what was said)
    if conversation:
        

        for msg in conversation:
            role = (msg.get("role") or "user").upper()
            content = msg.get("content") or ""

            # Example format:
            # USER: Hello
            # ASSISTANT: Hi, how can I help?
            sections.append(f"{role}: {content}")
    else:
        sections.append("No recent conversation.")

    # -----------------------------
    # 5. User Question
    # -----------------------------
    # This is the new question the user just asked.
    # The AI must answer this question.
    sections.append("\n### USER QUESTION")
    sections.append(user_query.strip())


     # -----------------------------
    # 6. Instruction (VERY IMPORTANT 🔥)
    # -----------------------------
    sections.append("\n### INSTRUCTION")
    sections.append("""
    Use the conversation and past experience to answer.
    Do not make up facts.
    If unsure, say you don't know.
    """)

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
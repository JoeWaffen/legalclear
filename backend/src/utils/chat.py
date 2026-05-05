from typing import List, Dict, Any

def append_chat_history(messages: List[Dict[str, Any]], chat_history: List[Dict[str, Any]]) -> None:
    """
    Appends chat history messages to the messages list in-place.
    Extracts only 'role' and 'content' fields, defaulting to 'user' and '' respectively.
    """
    for msg in chat_history:
        messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", "")
        })

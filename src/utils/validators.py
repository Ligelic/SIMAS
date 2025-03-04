def validate_message_content(content):
    if not isinstance(content, str):
        raise ValueError("Message content must be a string.")
    if len(content) == 0:
        raise ValueError("Message content cannot be empty.")
    if len(content) > 500:
        raise ValueError("Message content cannot exceed 500 characters.")
    return True

def validate_agent_configuration(config):
    required_keys = ['name', 'type', 'settings']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    return True

def validate_chat_room_capacity(capacity):
    if not isinstance(capacity, int) or capacity <= 0:
        raise ValueError("Chat room capacity must be a positive integer.")
    return True
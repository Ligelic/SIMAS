def log_message(message, level="INFO"):
    levels = {
        "INFO": "[INFO]",
        "WARNING": "[WARNING]",
        "ERROR": "[ERROR]",
        "DEBUG": "[DEBUG]"
    }
    
    if level not in levels:
        raise ValueError("Invalid log level. Choose from: INFO, WARNING, ERROR, DEBUG.")
    
    print(f"{levels[level]} {message}")
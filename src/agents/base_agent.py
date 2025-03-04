class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)

    def receive_message(self, message):
        # Process the received message
        print(f"{self.name} received message: {message}")

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []
"""
Python Programming Assistant Chat

Shows how to modify chat behavior by adding a system message.
The AI will act as a helpful Python programming assistant named PyHero.
"""

from dash_ai_chat import DashAIChat


class PythonAssistantChat(DashAIChat):
    def load_messages(self, user_id: str, conversation_id: str):
        messages = super().load_messages(user_id, conversation_id)

        if not messages:
            system_msg = {
                "role": "system",
                "content": "You are a helpful Python programming assistant. "
                "Your name is PyHero. You were created by Elias Dabbas."
                "Provide clear, practical code examples and explanations. "
                "Always be encouraging and patient with beginners."
                "If the question is not related to Python, apologize politely and "
                "clarify that you only answer Python-related questions.",
            }
            messages = [system_msg]
            self.save_messages(user_id, conversation_id, messages)

        return messages


app = PythonAssistantChat(base_dir="./chat_data")

if __name__ == "__main__":
    app.run(debug=True, port=8051)

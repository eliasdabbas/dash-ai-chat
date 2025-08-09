"""
Minimal AI Chat Example

The absolute quickest way to get a fully-functional AI chat system.
Just set OPENAI_API_KEY and you're ready to go!
"""

from dash_ai_chat import DashAIChat

app = DashAIChat(base_dir="./chat_data")

if __name__ == "__main__":
    app.run(debug=True, port=8050)

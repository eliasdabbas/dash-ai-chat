"""
Gemini Provider Example

Shows how easy it is to use Google's Gemini AI provider instead of OpenAI.
Just set the provider_spec and provider_model in the constructor!
"""

from dash_ai_chat import DashAIChat

# Simply configure Gemini provider at initialization - that's it!
app = DashAIChat(
    base_dir="./chat_data",
    provider_spec="gemini:chat.completions",
    provider_model="gemini-2.5-flash",
)

if __name__ == "__main__":
    app.run(debug=True, port=8053)

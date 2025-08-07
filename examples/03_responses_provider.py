"""
Different Provider Example

Shows how to use different AI providers and models.
This example uses OpenAI's responses API instead of chat completions.
"""

from dash_ai_chat import DashAIChat


class ResponsesChat(DashAIChat):
    def update_convo(
        self,
        user_id: str,
        user_message: str,
        convo_id=None,
        provider_spec="openai:responses",
    ):
        return super().update_convo(
            user_id,
            user_message,
            convo_id,
            provider_spec=provider_spec,
        )


app = ResponsesChat(base_dir="./chat_data")

if __name__ == "__main__":
    app.run(debug=True, port=8053)
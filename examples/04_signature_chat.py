"""
Signature Chat with Token Usage

This example demonstrates how to:
1. Extract token usage from raw API responses
2. Add custom signatures to assistant messages
3. Create professional layouts with flexbox
"""

from dash import html
from dash_ai_chat import DashAIChat


class SignatureChat(DashAIChat):
    def get_token_usage_list(self, user_id, conversation_id):
        """Extract token usage from each API response."""
        responses_file = (
            self._get_convo_dir(user_id, conversation_id) / "raw_api_responses.jsonl"
        )
        if not responses_file.exists():
            return []

        usage_list = []
        for response in self._read_jsonl(responses_file):
            if "usage" in response:
                usage = response["usage"]
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)
                total = usage.get("total_tokens", prompt_tokens + completion_tokens)
                model = response.get("model", "unknown")

                token_display = f"{prompt_tokens}↑ + {completion_tokens}↓ = {total} tokens | {model}"
                usage_list.append(token_display)
            else:
                usage_list.append("")  # No usage data available

        return usage_list

    def format_messages(self, messages):
        from dash import callback_context, html

        formatted = super().format_messages(messages)

        # Extract user and conversation from URL (e.g., /user123/001)
        url_path = callback_context.inputs.get("url.pathname", "")
        path_parts = url_path.strip("/").split("/")

        if len(path_parts) >= 2:
            user_folder = f"chat_data/{path_parts[0]}"  # Match directory structure
            conversation_id = path_parts[1]
            token_usage_list = self.get_token_usage_list(user_folder, conversation_id)
        else:
            token_usage_list = []

        assistant_index = 0
        for msg_index, message in enumerate(messages):
            if message["role"] == "assistant":
                token_display = (
                    token_usage_list[assistant_index]
                    if assistant_index < len(token_usage_list)
                    else ""
                )
                assistant_index += 1

                signature = html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    token_display,
                                    style={
                                        "font-family": "monospace",
                                        "font-size": "0.95em",
                                        "color": "#333",
                                        "font-weight": "500",
                                        "align-self": "flex-end",
                                    },
                                )
                                if token_display
                                else None,
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                "Sincerely, ",
                                                html.A(
                                                    "DashAIChat! 🤖",
                                                    href="https://pypi.org/project/dash-ai-chat/",
                                                    target="_blank",
                                                ),
                                            ],
                                            style={
                                                "font-style": "italic",
                                                "margin-bottom": "5px",
                                            },
                                        ),
                                        html.Code(
                                            "pip install dash-ai-chat",
                                            style={
                                                "background-color": "#f8f9fa",
                                                "padding": "2px 4px",
                                                "border-radius": "3px",
                                                "font-size": "0.8em",
                                            },
                                        ),
                                    ],
                                    style={"text-align": "right"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "space-between",
                                "align-items": "flex-end",
                                "margin-top": "15px",
                                "padding-bottom": "10px",
                                "border-bottom": "1px solid #eee",
                                "color": "#666",
                            },
                        ),
                        html.Br(),
                    ]
                )

                # Append the signature to the children of the formatted assistant message
                # (Assumes the first child is the Markdown message)
                if hasattr(formatted[msg_index], "children") and isinstance(
                    formatted[msg_index].children, list
                ):
                    formatted[msg_index].children.append(signature)

        return formatted


app = SignatureChat(base_dir="./chat_data")


if __name__ == "__main__":
    app.run(debug=True, port=8054)

"""
Custom Provider with Signature

Shows how to create a custom provider that modifies responses.
This example adds a styled signature to every AI response.
"""

from dash import html
from dash_ai_chat import DashAIChat


class SignatureChat(DashAIChat):
    def format_messages(self, messages):
        formatted = super().format_messages(messages)

        for i, msg in enumerate(messages):
            if msg["role"] == "assistant":
                signature_div = html.Div(
                    [
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
                                    style={"font-style": "italic"},
                                ),
                                html.Code(
                                    "pip install dash-ai-chat",
                                    style={
                                        "background-color": "#f8f9fa",
                                        "padding": "2px 4px",
                                        "border-radius": "3px",
                                        "font-size": "0.8em",
                                        "font-style": "normal",
                                    },
                                ),
                            ],
                            style={
                                "text-align": "right",
                                "font-size": "0.9em",
                                "color": "#666",
                                "margin-top": "15px",
                                "padding-bottom": "10px",
                                "border-bottom": "1px solid #eee",
                            },
                        ),
                        html.Br(),
                    ]
                )

                if i < len(formatted):
                    formatted[i].children.append(signature_div)

        return formatted


app = SignatureChat(base_dir="./chat_data")

if __name__ == "__main__":
    app.run(debug=True, port=8054)

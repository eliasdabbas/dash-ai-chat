"""
Custom Layout with Disclaimer

Shows how to customize the UI by adding a disclaimer under the input area.
Demonstrates layout modification without breaking existing functionality.
"""

from dash import html
from dash_ai_chat import DashAIChat


class DisclaimerChat(DashAIChat):
    def input_area(self):
        original_input = super().input_area()

        disclaimer = html.Div(
            [
                html.I(className="bi bi-info-circle", style={"margin-right": "5px"}),
                "AI can make mistakes. Please verify important information.",
            ],
            style={
                "font-size": "0.9em",
                "color": "#666",
                "margin-top": "5px",
                "text-align": "center",
            },
        )

        return html.Div([original_input, disclaimer, html.Br()])


app = DisclaimerChat(base_dir="./chat_data")

if __name__ == "__main__":
    app.run(debug=True, port=8052)

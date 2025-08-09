"""
Interactive Components Example

Shows how to add interactive Dash components (dropdowns, buttons) to AI responses.
The last assistant message gets a color picker dropdown for enhanced interactivity.
"""

import uuid

from dash import ALL, Input, Output, dcc, html, no_update
from dash_ai_chat import DashAIChat


class InteractiveChat(DashAIChat):
    def format_messages(self, messages):
        formatted = super().format_messages(messages)

        assistant_indices = []
        for i, msg in enumerate(messages):
            if msg["role"] == "assistant":
                assistant_indices.append(i)

        if assistant_indices:
            last_assistant_idx = assistant_indices[-1]

            interactive_component = html.Div(
                [
                    html.H6(
                        "Which color would you like to learn about?",
                        style={"color": "#495057", "margin-bottom": "10px"},
                    ),
                    dcc.Dropdown(
                        id={"type": "color-dropdown", "index": last_assistant_idx},
                        options=[
                            {"label": "🔴 Red", "value": "red"},
                            {"label": "🔵 Blue", "value": "blue"},
                            {"label": "🟢 Green", "value": "green"},
                            {"label": "🟡 Yellow", "value": "yellow"},
                            {"label": "🟣 Purple", "value": "purple"},
                            {"label": "🟠 Orange", "value": "orange"},
                            {"label": "🟤 Brown", "value": "brown"},
                            {"label": "⚫ Black", "value": "black"},
                            {"label": "⚪ White", "value": "white"},
                            {"label": "🩷 Pink", "value": "pink"},
                        ],
                        placeholder="Select a color to explore...",
                        style={"margin-bottom": "15px"},
                    ),
                ],
                style={
                    "background-color": "#f8f9fa",
                    "padding": "15px",
                    "border-radius": "10px",
                    "margin-top": "15px",
                    "border": "1px solid #dee2e6",
                },
            )

            if last_assistant_idx < len(formatted):
                formatted[last_assistant_idx].children.append(interactive_component)

        return formatted


app = InteractiveChat(base_dir="./chat_data")


@app.callback(
    [
        Output("user_input_textarea", "value", allow_duplicate=True),
        Output("user_input_textarea", "n_submit", allow_duplicate=True),
    ],
    Input({"type": "color-dropdown", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def handle_color_selection(selected_colors):
    if not selected_colors or not any(selected_colors):
        return no_update, no_update

    selected_color = next(c for c in selected_colors if c)

    color_message = f"""Analyze the color {selected_color} from a marketing and 
branding perspective.

Please address these three key areas:

**Market Positioning**: Which 2-3 industries commonly use this color and why?
**Consumer Psychology**: How does this color influence purchasing decisions? 
(1-2 key effects)  
**Competitive Advantage**: What unique marketing opportunity does this color 
provide?

Keep response concise - aim for 2-3 sentences per section.

Start your response with the heading "# The Color {selected_color.title()}" """

    return color_message, 1


if __name__ == "__main__":
    app.run(debug=True, port=8057)

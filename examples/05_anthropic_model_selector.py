"""
Anthropic Model Selector Example

Shows how easy it is to configure and switch Claude models with the new hybrid approach.
Demonstrates both constructor configuration and runtime switching.
"""

from dash import Input, dcc, html
from dash_ai_chat import DashAIChat

# Dropdown for model selection
model_dropdown = dcc.Dropdown(
    id="model_dropdown",
    options=[
        {
            "label": "🧠 Claude 3.5 Sonnet (Most Capable)",
            "value": "claude-3-5-sonnet-20241022",
        },
        {
            "label": "⚡ Claude 3.5 Haiku (Fast & Efficient)",
            "value": "claude-3-5-haiku-20241022",
        },
        {
            "label": "🎯 Claude 3 Opus (Creative & Detailed)",
            "value": "claude-3-opus-20240229",
        },
    ],
    value="claude-3-5-sonnet-20241022",  # Default selection
    clearable=False,
    style={"width": "60%", "margin-bottom": "15px"},
)


class AnthropicModelSelector(DashAIChat):
    def default_layout(self):
        base_layout = super().default_layout()
        model_selector_row = html.Div(
            [
                html.Div(
                    [model_dropdown],
                    className="col-lg-7 col-md-12 mx-auto",
                )
            ],
            className="row justify-content-center",
        )
        # Insert the model selector row as a top-level child above the input area
        children = list(base_layout.children)
        input_area_idx = None
        for idx, child in enumerate(children):
            # Only check first-level children for the textarea id
            if getattr(child, "id", None) == "user_input_textarea":
                input_area_idx = idx
                break
        if input_area_idx is None:
            input_area_idx = len(children) - 1
        children.insert(input_area_idx, model_selector_row)
        children.append(html.Br())
        children.append(html.Br())
        base_layout.children = children
        return base_layout


# Configure Anthropic provider at initialization, model selection via dropdown
app = AnthropicModelSelector(
    base_dir="./chat_data",
    provider_spec="anthropic:chat.completions",
    provider_model="claude-3-5-sonnet-20241022",
)


@app.callback(
    Input("model_dropdown", "value"),
)
def update_model_selection(selected_model):
    # Simple runtime model switching - just update the instance attribute!
    app.provider_model = selected_model


if __name__ == "__main__":
    app.run(debug=True, port=8055)

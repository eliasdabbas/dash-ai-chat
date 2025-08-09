"""
Runtime Provider/Model Switching Example

Demonstrates dynamic switching between different AI providers and models at runtime.
Shows how easy it is to change providers (OpenAI, Anthropic, Gemini) with simple attribute assignment.
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from dash_ai_chat import DashAIChat


class MultiProviderChat(DashAIChat):
    def default_layout(self):
        base_layout = super().default_layout()

        # Add provider and model selectors
        selector_row = html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label(
                                            "AI Provider:",
                                            style={
                                                "font-weight": "bold",
                                                "margin-bottom": "5px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="provider_dropdown",
                                            options=[
                                                {
                                                    "label": "🤖 OpenAI",
                                                    "value": "openai:chat.completions",
                                                },
                                                {
                                                    "label": "🧠 Anthropic",
                                                    "value": "anthropic:chat.completions",
                                                },
                                                {
                                                    "label": "💎 Gemini",
                                                    "value": "gemini:chat.completions",
                                                },
                                            ],
                                            value="openai:chat.completions",
                                            clearable=False,
                                            style={"margin-bottom": "10px"},
                                        ),
                                    ],
                                    className="col-md-6",
                                ),
                                html.Div(
                                    [
                                        html.Label(
                                            "Model:",
                                            style={
                                                "font-weight": "bold",
                                                "margin-bottom": "5px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="model_dropdown",
                                            value="gpt-4o",
                                            clearable=False,
                                            style={"margin-bottom": "15px"},
                                        ),
                                    ],
                                    className="col-md-6",
                                ),
                            ],
                            className="row",
                        )
                    ],
                    className="col-lg-7 col-md-12 mx-auto",
                )
            ],
            className="row justify-content-center",
            style={"margin-bottom": "20px"},
        )

        # Place selector_row as a top-level child above the user input area
        children = list(base_layout.children)
        input_area_idx = None
        for idx, child in enumerate(children):
            if getattr(child, "id", None) == "user_input_textarea":
                input_area_idx = idx
                break
        if input_area_idx is None:
            input_area_idx = len(children) - 1
        children.insert(input_area_idx, selector_row)
        base_layout.children = children

        # Add dbc class for dash-bootstrap-components styling
        # Set className attribute on the main div for global Bootstrap styling
        current_classes = getattr(base_layout, "className", "") or ""
        base_layout.className = f"{current_classes} dbc".strip()
        return base_layout


# apply Bootstrap styles to Dash core components:
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = MultiProviderChat(
    base_dir="./chat_data",
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP, dbc_css],
)


@app.callback(
    [Output("model_dropdown", "options"), Output("model_dropdown", "value")],
    Input("provider_dropdown", "value"),
)
def update_provider_and_models(provider_spec):
    """Switch AI provider and update available models based on selected provider."""
    app.provider_spec = provider_spec

    # Return model options based on the provider_spec input
    if provider_spec == "openai:chat.completions":
        model_options = [
            {"label": "GPT-4o", "value": "gpt-4o"},
            {"label": "GPT-4o Mini", "value": "gpt-4o-mini"},
            {"label": "GPT-3.5 Turbo", "value": "gpt-3.5-turbo"},
        ]
        default_model = "gpt-4o"
    elif provider_spec == "anthropic:chat.completions":
        model_options = [
            {"label": "Claude 3.5 Sonnet", "value": "claude-3-5-sonnet-20241022"},
            {"label": "Claude 3.5 Haiku", "value": "claude-3-5-haiku-20241022"},
            {"label": "Claude 3 Opus", "value": "claude-3-opus-20240229"},
        ]
        default_model = "claude-3-5-sonnet-20241022"
    elif provider_spec == "gemini:chat.completions":
        model_options = [
            {"label": "Gemini 2.5 Flash", "value": "gemini-2.5-flash"},
            {"label": "Gemini 1.5 Pro", "value": "gemini-1.5-pro"},
        ]
        default_model = "gemini-2.5-flash"
    else:
        model_options = []
        default_model = ""

    # Update app's model to the provider default
    app.provider_model = default_model
    return model_options, default_model


@app.callback(
    Input("model_dropdown", "value"),
)
def update_model(model):
    if model:
        app.provider_model = model


if __name__ == "__main__":
    app.run(debug=True, port=8056)

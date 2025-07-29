from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html


class DashAIChat(Dash):
    def __init__(self, name=__name__, external_stylesheets=None, **kwargs):
        if external_stylesheets is None:
            external_stylesheets = [dbc.themes.BOOTSTRAP]
        super().__init__(name, external_stylesheets=external_stylesheets, **kwargs)
        self.required_ids = {
            "burger_menu",
            "sidebar_offcanvas",
            "conversation_list",
            "url",
            "chat_area_div",
            "user_input_textarea",
            "new_chat_button",
        }
        self.BASE_DIR = Path("")
        self.AI_REGISTRY = {
            ("openai", "chat.completions"): {
                "call": lambda messages,
                model,
                **kwargs: self.client.chat.completions.create(
                    model=model, messages=messages, **kwargs
                ),
                "extract": lambda resp: resp["choices"][0]["message"]["content"],
                "format_messages": lambda history: [
                    {"role": m["role"], "content": m["content"]} for m in history
                ],
            },
            ("openai", "completions"): {
                "call": lambda prompt, model, **kwargs: self.client.completions.create(
                    model=model, prompt=prompt, **kwargs
                ),
                "extract": lambda resp: resp["choices"][0]["text"],
                "format_messages": lambda history: "\n".join(
                    f"{m['role']}: {m['content']}" for m in history
                ),
            },
        }
        self.layout = self.default_layout()
        self._validate_layout()
        # self._register_callbacks()
        # self._register_clientside_callbacks()

    # --- Layout Factories ---
    def sidebar(self):
        return dbc.Offcanvas(
            [
                html.Div(
                    [
                        html.I(className="bi bi-pencil-square icon-new-chat"),
                        " New chat",
                    ],
                    id="new_chat_button",
                    className="mb-3 w-100",
                ),
                html.Div(
                    id="conversation_list",
                    children=[],
                ),
            ],
            id="sidebar_offcanvas",
            title="Conversations",
            is_open=False,
            placement="start",
        )

    def chat_area(self):
        return html.Div(
            id="chat_area_div",
            children=[],
            className="chat-area-div",
        )

    def input_area(self):
        return html.Div(
            [
                dbc.Textarea(
                    id="user_input_textarea",
                    placeholder="Ask...",
                    rows=4,
                    autoFocus=True,
                    className="form-control user-input-textarea",
                ),
            ]
        )

    def default_layout(self):
        return html.Div(
            [
                html.Button(
                    "☰",
                    id="burger_menu",
                    className="burger-menu btn btn-outline-secondary",
                ),
                self.sidebar(),
                dcc.Location(id="url", refresh=False),
                html.Div(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.Div(
                                    [dcc.Loading(self.chat_area(), type="circle")],
                                    className="col",
                                )
                            ],
                            className="row",
                        ),
                        html.Div(
                            [html.Div([self.input_area()], className="col")],
                            className="row",
                        ),
                    ],
                    className="container main-container",
                ),
            ]
        )

    def _validate_layout(self):
        def collect_ids(component):
            ids = set()
            if hasattr(component, "id") and component.id:
                ids.add(component.id)
            if hasattr(component, "children"):
                children = component.children
                if isinstance(children, list):
                    for child in children:
                        ids |= collect_ids(child)
                elif children is not None:
                    ids |= collect_ids(children)
            return ids

        ids = collect_ids(self.layout)
        missing = self.required_ids - ids
        if missing:
            raise ValueError(
                f"The following required component IDs are missing from the layout: {missing}"
            )

    def set_layout(self, layout):
        self.layout = layout
        self._validate_layout()

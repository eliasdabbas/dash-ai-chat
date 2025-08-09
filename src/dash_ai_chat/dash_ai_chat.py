import datetime
import json
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

import dash_bootstrap_components as dbc
from dash import ALL, Dash, Input, Output, State, callback_context, dcc, html, no_update

from .providers import build_default_registry


class DashAIChat(Dash):
    def __init__(
        self,
        base_dir,
        provider_spec="openai:chat.completions",
        provider_model="gpt-4o",
        **kwargs,
    ):
        if "external_stylesheets" not in kwargs:
            kwargs["external_stylesheets"] = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]

        assets_path = (Path(__file__).parent / "assets").absolute()
        if "assets_folder" not in kwargs:
            kwargs["assets_folder"] = str(assets_path)

        super().__init__(
            __name__,
            **kwargs,
        )
        self.required_ids = {
            "burger_menu",
            "sidebar_offcanvas",
            "conversation_list",
            "url",
            "chat_area_div",
            "user_input_textarea",
            "new_chat_button",
        }
        self.BASE_DIR = Path(base_dir)
        self.AI_REGISTRY = build_default_registry()
        self.provider_spec = provider_spec
        self.provider_model = provider_model
        self.layout = self.default_layout()
        self._validate_layout()
        self._register_callbacks()
        self._register_clientside_callbacks()

    # --- Layout Components ---
    def header(self):
        """App header with navigation toggle button.

        Override to add branding, user menu, or other header elements.
        """
        burger_menu = html.Button(
            "☰",
            id="burger_menu",
            className="burger-menu",
        )
        return html.Div([burger_menu])

    def sidebar(self):
        """Sidebar panel with conversations and new chat button.

        Override to add tabs, settings, or reorganize navigation.
        """
        new_chat_button = html.Div(
            [
                html.I(className="bi bi-pencil-square icon-new-chat"),
                " New chat",
            ],
            id="new_chat_button",
            className="new-chat-button",
        )

        conversations = html.Div(
            id="conversation_list",
            children=[],
            className="conversation-list",
        )

        return dbc.Offcanvas(
            [new_chat_button, conversations],
            id="sidebar_offcanvas",
            is_open=False,
            backdrop=False,
            placement="start",
            className="sidebar-offcanvas",
        )

    def chat_area(self):
        """Main conversation display area.

        Override to add message filtering, search, or custom message rendering.
        """
        return html.Div(
            [
                html.Div(
                    id="chat_area_div",
                    children=[],
                    className="chat-area-div",
                )
            ],
            className="col-lg-7 col-md-12 mx-auto mt-4 px-4",
        )

    def input_area(self):
        """Message input area.

        Override to add send buttons, attachment tools, or formatting options.
        """
        textarea = dbc.Textarea(
            id="user_input_textarea",
            placeholder="Ask...",
            rows=4,
            autoFocus=True,
            className="form-control user-input-textarea",
        )
        return html.Div(
            [textarea],
            className="col-lg-7 col-md-12 mx-auto",
        )

    def default_layout(self):
        """Default app layout with flat, hackable structure.

        Components are organized as independent, easily customizable sections:
        - header(): Navigation and branding area
        - sidebar(): Conversations and navigation panel
        - chat_area(): Main conversation display (with loading)
        - input_area(): Message input section

        Override this method or individual components to customize the layout.
        """
        return html.Div(
            [
                dcc.Location(id="url", refresh=False),
                self.header(),
                self.sidebar(),
                dcc.Loading(
                    self.chat_area(),
                    type="circle",
                    overlay_style={
                        "visibility": "visible",
                        "filter": "blur(0.7px)",
                    },
                ),
                self.input_area(),
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

    # --- Engine Methods (to be overridden as needed) ---
    def load_messages(self, user_id: str, conversation_id: str) -> List[Dict]:
        path = self._get_convo_dir(user_id, conversation_id) / "messages.json"
        return self._read_json(path) if path.exists() else []

    def save_messages(
        self, user_id: str, conversation_id: str, messages: List[Dict]
    ) -> None:
        path = self._ensure_convo_dir(user_id, conversation_id) / "messages.json"
        self._write_json(path, messages)

    def add_message(self, user_id: str, conversation_id: str, message: Dict) -> None:
        messages = self.load_messages(user_id, conversation_id)
        messages.append(message)
        self.save_messages(user_id, conversation_id, messages)

    def append_raw_response(
        self, user_id: str, conversation_id: str, response: Dict
    ) -> None:
        path = (
            self._ensure_convo_dir(user_id, conversation_id) / "raw_api_responses.jsonl"
        )
        self._append_jsonl(path, response)

    def load_metadata(self, user_id: str, conversation_id: str) -> Dict:
        path = self._get_convo_dir(user_id, conversation_id) / "metadata.json"
        return self._read_json(path) if path.exists() else {}

    def save_metadata(self, user_id: str, conversation_id: str, metadata: Dict) -> None:
        path = self._ensure_convo_dir(user_id, conversation_id) / "metadata.json"
        self._write_json(path, metadata)

    def list_users(self) -> List[str]:
        return sorted([p.name for p in self.BASE_DIR.iterdir() if p.is_dir()])

    def list_conversations(self, user_id: str) -> List[str]:
        user_dir = self._get_user_dir(user_id)
        if not user_dir.exists():
            return []
        return sorted([p.name for p in user_dir.iterdir() if p.is_dir()])

    def get_conversation_titles(self, user_id: str) -> List[Dict[str, str]]:
        conversations = self.list_conversations(user_id)
        result = []
        for convo_id in conversations:
            messages = self.load_messages(user_id, convo_id)
            if messages:
                first_message = messages[0].get("content", "")
                title = (
                    first_message[:30] + "..."
                    if len(first_message) > 30
                    else first_message
                )
                title = title.capitalize() if title else ""
                result.append({"id": convo_id, "title": title})
        return result

    def get_last_convo_id(self, user_id: str) -> Optional[str]:
        conversations = self.list_conversations(user_id)
        return conversations[-1] if conversations else self.get_next_convo_id(user_id)

    def get_next_convo_id(self, user_id: str) -> str:
        user_dir = self._get_user_dir(user_id)
        if not user_dir.exists():
            return "001"
        existing_ids = [
            int(p.name) for p in user_dir.iterdir() if p.is_dir() and p.name.isdigit()
        ]
        if not existing_ids:
            return "001"
        next_id = max(existing_ids) + 1
        return f"{next_id:03d}"

    def fetch_ai_response(
        self,
        messages: List[Dict],
        provider_spec: Optional[str] = None,
        provider_model: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        # Use instance defaults if not provided
        provider_spec = provider_spec or self.provider_spec
        provider_model = provider_model or self.provider_model

        if provider_spec not in self.AI_REGISTRY:
            raise ValueError(f"Unknown provider spec: {provider_spec}")
        if not provider_model:
            raise ValueError("Model must be specified explicitly.")

        provider = self.AI_REGISTRY[provider_spec]
        client = provider.client_factory()
        formatted_messages = provider.format_messages(messages)
        resp = provider.call(client, formatted_messages, provider_model, **kwargs)
        return resp.model_dump() if hasattr(resp, "model_dump") else resp

    def extract_assistant_content(
        self,
        raw_response: Dict,
        provider_spec: str = "openai:chat.completions",
    ) -> str:
        if provider_spec not in self.AI_REGISTRY:
            raise ValueError(f"Unknown provider spec: {provider_spec}")
        provider = self.AI_REGISTRY[provider_spec]
        return provider.extract(raw_response)

    def update_convo(
        self,
        user_id: str,
        user_message: str,
        convo_id: Optional[str] = None,
        provider_spec: Optional[str] = None,
        provider_model: Optional[str] = None,
    ) -> str:
        # Use instance defaults if not provided
        provider_spec = provider_spec or self.provider_spec
        provider_model = provider_model or self.provider_model

        convo_id = convo_id or self.get_next_convo_id(user_id)
        user_msg = {"role": "user", "content": user_message}
        self.add_message(user_id, convo_id, user_msg)
        history = self.load_messages(user_id, convo_id)
        raw_response = self.fetch_ai_response(
            history,
            provider_spec=provider_spec,
            provider_model=provider_model,
        )
        self.append_raw_response(user_id, convo_id, raw_response)
        assistant_content = self.extract_assistant_content(raw_response, provider_spec)
        assistant_msg = {"role": "assistant", "content": assistant_content}
        self.add_message(user_id, convo_id, assistant_msg)
        return convo_id

    def _register_callbacks(self):
        @self.callback(
            Output("chat_area_div", "children"),
            Output("user_input_textarea", "value"),
            Input("user_input_textarea", "n_submit"),
            Input("url", "pathname"),
            State("user_input_textarea", "value"),
        )
        def handle_user_input(n_submit, pathname, value):
            import uuid

            segments = (pathname or "/").strip("/").split("/")
            user_id = segments[0] if segments and segments[0] else str(uuid.uuid4())[:5]
            convo_id = segments[1] if len(segments) > 1 and segments[1] else None
            engine_user_id = f"chat_data/{user_id}"
            if not convo_id:
                convo_id = self.get_next_convo_id(engine_user_id)
            if n_submit and value:
                self.update_convo(
                    user_id=engine_user_id, user_message=value, convo_id=convo_id
                )
            messages = self.load_messages(engine_user_id, convo_id)
            return self.format_messages(messages), ""

        @self.callback(
            Output("sidebar_offcanvas", "is_open"),
            Output("url", "pathname", allow_duplicate=True),
            Input("burger_menu", "n_clicks"),
            Input({"type": "conversation-item", "index": ALL}, "n_clicks"),
            State("sidebar_offcanvas", "is_open"),
            State("url", "pathname"),
            prevent_initial_call=True,
        )
        def toggle_offcanvas_and_navigate(
            burger_clicks, convo_clicks, is_open, current_pathname
        ):
            ctx = callback_context
            if not ctx.triggered:
                return no_update, no_update
            trigger_id = ctx.triggered[0]["prop_id"]
            if "conversation-item" in trigger_id and any(convo_clicks):
                clicked_index = next(
                    i for i, clicks in enumerate(convo_clicks) if clicks and clicks > 0
                )
                convo_id = f"{clicked_index + 1:03d}"
                import re

                new_path = re.sub(r"/[^/]*$", f"/{convo_id}", current_pathname or "/")
                return False, new_path
            if "burger_menu" in trigger_id and burger_clicks:
                return not is_open, no_update
            return no_update, no_update

        @self.callback(
            Output("conversation_list", "children"),
            Input("url", "pathname"),
        )
        def update_conversation_list(pathname):
            import uuid

            if not pathname:
                return []
            segments = pathname.strip("/").split("/")
            user_id = segments[0] if segments and segments[0] else str(uuid.uuid4())[:5]
            engine_user_id = f"chat_data/{user_id}"
            conversations = self.get_conversation_titles(engine_user_id)
            if not conversations:
                return []
            conversation_items = []
            for convo in conversations:
                conversation_items.append(
                    html.Div(
                        convo["title"],
                        id={"type": "conversation-item", "index": convo["id"]},
                        style={
                            "cursor": "pointer",
                            "padding": "0.5rem",
                            "margin-bottom": "0.25rem",
                            "border-radius": "5px",
                        },
                    )
                )
            return conversation_items

        @self.callback(
            Output("url", "pathname", allow_duplicate=True),
            Output("sidebar_offcanvas", "is_open", allow_duplicate=True),
            Input("new_chat_button", "n_clicks"),
            State("url", "pathname"),
            prevent_initial_call=True,
        )
        def handle_new_chat(n_clicks, current_pathname):
            if n_clicks:
                import uuid

                segments = (current_pathname or "/").strip("/").split("/")
                user_id = (
                    segments[0] if segments and segments[0] else str(uuid.uuid4())[:5]
                )

                engine_user_id = f"chat_data/{user_id}"
                next_convo_id = self.get_next_convo_id(engine_user_id)
                new_path = f"/{user_id}/{next_convo_id}"

                return new_path, False
            return no_update, no_update

    def _register_clientside_callbacks(self):
        self.clientside_callback(
            """
            function(chat_content) {
                if (chat_content && chat_content.length > 0) {
                    setTimeout(() => {
                        const chatArea = document.getElementById('chat_area_div');
                        if (chatArea) {
                            chatArea.scrollTop = chatArea.scrollHeight;
                        }
                    }, 100);
                }
                return window.dash_clientside.no_update;
            }
            """,
            Output("chat_area_div", "data-scroll-trigger", allow_duplicate=True),
            Input("chat_area_div", "children"),
            prevent_initial_call=True,
        )
        self.clientside_callback(
            """
            function(textarea_value) {
                const textarea = document.getElementById('user_input_textarea');
                if (textarea && textarea_value) {
                    const rtlPattern = '[\u0590-\u05ff\u0600-\u06ff\u0750-\u077f' +
                                       '\u08a0-\u08ff\ufb1d-\ufb4f\ufb50-\ufdff\ufe70-\ufeff]';
                    const rtlRegex = new RegExp(rtlPattern);
                    const isRTL = rtlRegex.test(textarea_value);
                    textarea.style.direction = isRTL ? 'rtl' : 'ltr';
                    textarea.style.textAlign = isRTL ? 'right' : 'left';
                }
                return window.dash_clientside.no_update;
            }
            """,
            Output("user_input_textarea", "title", allow_duplicate=True),
            Input("user_input_textarea", "value"),
            prevent_initial_call=True,
        )

    # --- RTL Detection ---
    def _is_rtl(self, text):
        if not text or not text.strip():
            return False
        for char in text:
            bidi = unicodedata.bidirectional(char)
            if bidi in ("R", "AL"):
                return True
            elif bidi == "L":
                return False
        return False

    # --- Time ---
    def _now(self):
        return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")

    # --- Path Operations ---
    def _get_user_dir(self, user_id: str) -> Path:
        return self.BASE_DIR / user_id

    def _get_convo_dir(self, user_id: str, conversation_id: str) -> Path:
        return self._get_user_dir(user_id) / conversation_id

    def _ensure_convo_dir(self, user_id: str, conversation_id: str) -> Path:
        path = self._get_convo_dir(user_id, conversation_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    # --- File I/O ---
    def _read_json(self, path: Path) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _read_jsonl(self, path: Path) -> Iterator[Dict]:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def _write_json(self, path: Path, data: Any) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _append_jsonl(self, path: Path, entry: Dict) -> None:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def format_messages(self, messages):
        if not messages:
            return []
        formatted = []
        current_msg_direction = "ltr"
        for i, msg in enumerate(messages):
            if msg["role"] == "user":
                current_msg_direction = "rtl" if self._is_rtl(msg["content"]) else "ltr"
                formatted.append(
                    html.Div(
                        [
                            dcc.Markdown(
                                msg["content"],
                                id=f"user-msg-{i}",
                                style={
                                    "text-align": "right",
                                    "width": "80%",
                                    "margin-left": "auto",
                                    "padding": "0.3em 0.3em",
                                    "background-color": "var(--bs-light)",
                                    "border-radius": "15px",
                                },
                            ),
                            html.Div(
                                [
                                    dcc.Clipboard(
                                        content=msg["content"],
                                        id=f"clipboard-user-{i}",
                                        style={"cursor": "pointer"},
                                    ),
                                    dbc.Tooltip(
                                        "Copy",
                                        target=f"clipboard-user-{i}",
                                        placement="top",
                                    ),
                                ],
                                style={
                                    "text-align": "right",
                                    "width": "4%",
                                    "margin-left": "auto",
                                },
                            ),
                        ],
                        dir=current_msg_direction,
                    )
                )
            elif msg["role"] == "assistant":
                formatted.append(
                    html.Div(
                        [
                            dcc.Markdown(
                                msg["content"],
                                id=f"assistant-msg-{i}",
                                className="table table-striped table-hover",
                            ),
                            html.Div(
                                [
                                    dcc.Clipboard(
                                        content=msg["content"],
                                        id=f"clipboard-assistant-{i}",
                                        style={"cursor": "pointer"},
                                    ),
                                    dbc.Tooltip(
                                        "Copy",
                                        target=f"clipboard-assistant-{i}",
                                        placement="top",
                                    ),
                                ],
                                style={"width": "4%"},
                            ),
                        ],
                        dir=current_msg_direction,
                    )
                )
        return formatted

#!/usr/bin/env python3
"""
Zen Minimal Style Example

Demonstrates creative layout possibilities:
- Header integrated into chat area
- Floating sidebar
- Split-screen conversation view
- Minimalist aesthetic with creative positioning
"""

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_ai_chat import DashAIChat


class ZenMinimal(DashAIChat):
    """Ultra-minimal, zen-like AI chat interface with creative layout."""

    def header(self):
        """True zen - pure emptiness with floating navigation."""
        return html.Div(
            [
                # Floating burger menu - minimal and zen
                html.Button(
                    "☰",
                    id="burger_menu",
                    className="btn border-0 position-fixed",
                    style={
                        "top": "20px",
                        "left": "20px",
                        "fontSize": "3rem",
                        "background": "none",
                        "zIndex": 1000,
                        "color": "white",  # White for best contrast
                        "padding": "0",
                        "lineHeight": "1",
                        "textShadow": "2px 2px 8px rgba(0, 0, 0, 0.8)",
                        "filter": "drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2))",
                    },
                ),
            ]
        )

    def sidebar(self):
        """Floating, modern sidebar with glass morphism effect."""
        new_chat_button = html.Div(
            [
                html.Div(
                    [
                        html.I(className="bi bi-plus", style={"fontSize": "1.5rem"}),
                    ],
                    id="new_chat_button",
                    className="d-flex align-items-center justify-content-center rounded-circle bg-primary text-white mb-4",
                    style={"width": "50px", "height": "50px", "cursor": "pointer"},
                ),
            ]
        )

        conversations = html.Div(
            id="conversation_list",
            children=[],
            className="conversation-list-minimal",
        )

        return dbc.Offcanvas(
            [
                # Minimalist new chat
                new_chat_button,
                # Conversation history
                html.Div(
                    [
                        html.H6(
                            "Conversations",
                            className="fw-light mb-3",
                            style={"color": "rgba(255,255,255,0.8)"},
                        ),
                        conversations,
                    ]
                ),
            ],
            id="sidebar_offcanvas",
            is_open=False,
            backdrop=True,
            placement="start",
            style={
                "width": "280px",
                "background": "rgba(255, 255, 255, 0.1)",
                "backdropFilter": "blur(20px)",
                "border": "1px solid rgba(255, 255, 255, 0.2)",
                "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.3)",
                "color": "white",
            },
        )

    def chat_area(self):
        """Split conversation view with breathing room."""
        return html.Div(
            [
                # Spacer for floating header
                html.Div(style={"height": "80px"}),
                # Main conversation area
                html.Div(
                    id="chat_area_div",
                    children=[],
                    className="px-4",
                    style={
                        "maxWidth": "800px",
                        "margin": "0 auto",
                        "minHeight": "calc(100vh - 200px)",
                        "paddingBottom": "120px",  # Space for floating input
                        "background": "white",
                        "borderRadius": "12px",
                        "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.1)",
                    },
                ),
            ]
        )

    def input_area(self):
        """Floating input area at bottom with modern styling."""
        return html.Div(
            [
                html.Div(
                    [
                        # Input field
                        html.Div(
                            [
                                dbc.Textarea(
                                    id="user_input_textarea",
                                    placeholder="What's on your mind?",
                                    rows=1,
                                    className="border-0 bg-transparent",
                                    style={
                                        "resize": "none",
                                        "outline": "none",
                                        "boxShadow": "none",
                                        "fontSize": "1.1rem",
                                        "color": "#1a1a1a",
                                    },
                                ),
                            ],
                            className="flex-grow-1",
                        ),
                        # Send indicator (minimal)
                        html.Div(
                            [
                                html.I(
                                    className="bi bi-arrow-up-circle-fill",
                                    style={
                                        "fontSize": "1.5rem",
                                        "cursor": "pointer",
                                        "color": "white",
                                        "opacity": "0.8",
                                    },
                                )
                            ]
                        ),
                    ],
                    className="d-flex align-items-center p-4 rounded-pill shadow-lg",
                    style={
                        "background": "rgba(255, 255, 255, 0.6)",
                        "backdropFilter": "blur(20px)",
                        "border": "1px solid rgba(255, 255, 255, 0.3)",
                        "maxWidth": "600px",
                        "margin": "0 auto",
                        "color": "white",
                    },
                ),
            ],
            className="position-fixed bottom-0 start-0 end-0 p-4",
            style={"zIndex": 1000},
        )

    def tools_area(self):
        """Floating tools panel (bonus component!)."""
        return html.Div(
            [
                html.Div(
                    [
                        # Tool buttons
                        html.Div(
                            [
                                html.I(
                                    className="bi bi-camera text-muted p-2 rounded-circle bg-light me-2",
                                    style={"cursor": "pointer"},
                                ),
                                html.I(
                                    className="bi bi-mic text-muted p-2 rounded-circle bg-light me-2",
                                    style={"cursor": "pointer"},
                                ),
                                html.I(
                                    className="bi bi-paperclip text-muted p-2 rounded-circle bg-light",
                                    style={"cursor": "pointer"},
                                ),
                            ],
                            className="d-flex",
                        ),
                    ],
                    className="p-3 rounded-3 shadow-sm",
                    style={
                        "background": "rgba(255, 255, 255, 0.9)",
                        "backdropFilter": "blur(10px)",
                        "border": "1px solid rgba(255, 255, 255, 0.3)",
                    },
                ),
            ],
            className="position-fixed bottom-20 end-0 me-4",
            style={"zIndex": 999},
        )

    def default_layout(self):
        """Zen layout: floating elements, breathing room, minimal chrome."""
        return html.Div(
            [
                dcc.Location(id="url", refresh=False),
                # Background gradient
                html.Div(
                    className="position-fixed top-0 start-0 w-100 h-100",
                    style={
                        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        "zIndex": -1,
                    },
                ),
                # Floating header
                self.header(),
                # Hidden sidebar (slides in)
                self.sidebar(),
                # Main chat area
                dcc.Loading(
                    self.chat_area(),
                    type="dot",
                    color="#667eea",
                    style={"background": "transparent"},
                ),
                # Floating input
                self.input_area(),
                # Bonus: Floating tools
                self.tools_area(),
            ],
            style={"minHeight": "100vh", "fontFamily": "'Inter', sans-serif"},
        )


if __name__ == "__main__":
    app = ZenMinimal("chat_data")
    app.run(debug=True, port=8059)

"""
Corporate Dashboard Style Example

Demonstrates how the flat layout enables:
- Full corporate header with branding and navigation
- Professional sidebar with user info
- Status footer with system info
- Multi-panel layout
"""

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_ai_chat import DashAIChat


class CorporateDashboard(DashAIChat):
    """Premium enterprise AI assistant with sophisticated corporate branding."""

    def disclaimer_banner(self):
        """Display notice that elements are for demonstration only."""
        return html.Div(
            [
                html.P(
                    [
                        html.I(className="bi bi-info-circle me-2"),
                        "This is a UI demonstration of layout customization capabilities. ",
                        "All interface elements, navigation, and controls are for visual display only and are not functional.",
                    ],
                    className="mb-0 text-muted small",
                )
            ],
            className="alert alert-light border-0 rounded-0 py-2 text-center",
        )

    def header(self):
        """Premium corporate header with sophisticated branding and navigation."""
        return html.Header(
            [
                # Sophisticated navbar with gradient
                html.Nav(
                    [
                        html.Div(
                            [
                                # Premium brand section
                                html.Div(
                                    [
                                        # Elegant logo placeholder
                                        html.Div(
                                            [
                                                html.Span(
                                                    "⟐",
                                                    className="me-2",
                                                    style={
                                                        "fontSize": "1.8rem",
                                                        "color": "#C8A951",
                                                    },
                                                ),
                                                html.Span(
                                                    "DashAI",
                                                    className="fw-bold",
                                                    style={
                                                        "fontSize": "1.1rem",
                                                        "letterSpacing": "2px",
                                                        "color": "white",
                                                    },
                                                ),
                                                html.Span(
                                                    "Intelligence",
                                                    className="ms-1",
                                                    style={
                                                        "fontSize": "0.9rem",
                                                        "color": "#C8A951",
                                                        "fontWeight": "300",
                                                    },
                                                ),
                                            ],
                                            className="d-flex align-items-center",
                                        ),
                                    ],
                                    className="flex-grow-1",
                                ),
                                # Premium navigation
                                html.Div(
                                    [
                                        html.A(
                                            "Intelligence",
                                            href="#",
                                            className="text-white text-decoration-none me-4",
                                            style={
                                                "opacity": "0.9",
                                                "transition": "all 0.3s ease",
                                            },
                                        ),
                                        html.A(
                                            "Analytics",
                                            href="#",
                                            className="text-white text-decoration-none me-4",
                                            style={
                                                "opacity": "0.9",
                                                "transition": "all 0.3s ease",
                                            },
                                        ),
                                        html.A(
                                            "Insights",
                                            href="#",
                                            className="text-white text-decoration-none me-4",
                                            style={
                                                "opacity": "0.9",
                                                "transition": "all 0.3s ease",
                                            },
                                        ),
                                    ],
                                    className="d-none d-md-flex align-items-center",
                                ),
                                # Executive user section
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="https://pbs.twimg.com/profile_images/1873860106762289152/1aXokUPF_400x400.jpg",
                                                    className="rounded-circle me-2",
                                                    style={
                                                        "width": "32px",
                                                        "height": "32px",
                                                        "objectFit": "cover",
                                                    },
                                                ),
                                                html.Span(
                                                    "E. Dabbas",
                                                    className="text-white me-3 d-none d-sm-inline",
                                                ),
                                            ],
                                            className="d-flex align-items-center me-3",
                                        ),
                                        # Menu toggle with premium styling
                                        html.Button(
                                            "☰",
                                            id="burger_menu",
                                            className="btn text-white border-0",
                                            style={
                                                "background": "none",
                                                "fontSize": "1.8rem",
                                                "padding": "8px 12px",
                                                "lineHeight": "1",
                                            },
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                            ],
                            className="d-flex align-items-center px-4 py-3 w-100",
                        )
                    ],
                    style={
                        "background": "linear-gradient(135deg, #0A1F44 0%, #133B7A 50%, #0A1F44 100%)",
                        "boxShadow": "0 4px 20px rgba(0,0,0,0.15)",
                        "borderBottom": "1px solid rgba(200, 169, 81, 0.2)",
                    },
                )
            ]
        )

    def sidebar(self):
        """Executive-grade sidebar with premium styling and organized sections."""
        # Executive profile section
        executive_profile = html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src="https://pbs.twimg.com/profile_images/1873860106762289152/1aXokUPF_400x400.jpg",
                                    className="rounded-circle",
                                    style={
                                        "width": "64px",
                                        "height": "64px",
                                        "objectFit": "cover",
                                        "border": "3px solid #C8A951",
                                    },
                                ),
                            ],
                            className="text-center mb-3",
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "Elias Dabbas",
                                    className="mb-1 text-center",
                                    style={"color": "#0A1F44"},
                                ),
                                html.P(
                                    "Founder & AI Strategist",
                                    className="text-center mb-2 small",
                                    style={"color": "#4B5563"},
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "●",
                                            className="text-success me-1",
                                            style={"fontSize": "0.7rem"},
                                        ),
                                        html.Small(
                                            "Active", style={"color": "#4B5563"}
                                        ),
                                    ],
                                    className="text-center",
                                ),
                            ]
                        ),
                    ],
                    className="p-4",
                    style={
                        "background": "linear-gradient(135deg, #f8f9ff 0%, #e8eaf6 100%)",
                        "borderRadius": "12px",
                        "border": "1px solid rgba(10, 31, 68, 0.1)",
                    },
                )
            ],
            className="mb-4",
        )

        # Premium new conversation button
        new_chat_button = html.Div(
            [
                html.Button(
                    [html.I(className="bi bi-plus-lg me-2"), "New Analysis"],
                    id="new_chat_button",
                    className="w-100",
                    style={
                        "background": "linear-gradient(135deg, #0A1F44 0%, #133B7A 100%)",
                        "border": "none",
                        "color": "white",
                        "padding": "12px 24px",
                        "borderRadius": "8px",
                        "fontWeight": "500",
                        "boxShadow": "0 4px 12px rgba(10, 31, 68, 0.3)",
                        "transition": "all 0.3s ease",
                    },
                ),
            ],
            className="mb-4",
        )

        # Conversation sections
        conversation_sections = html.Div(
            [
                html.H6(
                    "Recent Intelligence",
                    className="text-uppercase small fw-bold mb-3",
                    style={"color": "#0A1F44", "letterSpacing": "1px"},
                ),
                html.Div(
                    id="conversation_list",
                    children=[],
                    className="conversation-list",
                ),
            ]
        )

        return dbc.Offcanvas(
            [
                executive_profile,
                new_chat_button,
                conversation_sections,
            ],
            id="sidebar_offcanvas",
            is_open=False,
            backdrop=False,
            placement="start",
            style={
                "width": "360px",
                "background": "linear-gradient(180deg, #ffffff 0%, #f8f9ff 100%)",
                "borderRight": "1px solid rgba(10, 31, 68, 0.1)",
                "boxShadow": "4px 0 20px rgba(0,0,0,0.1)",
            },
        )

    def chat_area(self):
        """Premium intelligence interface with sophisticated status monitoring."""
        return html.Div(
            [
                # Executive intelligence header
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.I(
                                            className="bi bi-brain me-2",
                                            style={
                                                "color": "#C8A951",
                                                "fontSize": "1.2rem",
                                            },
                                        ),
                                        html.H5(
                                            "DashAI Intelligence Engine",
                                            className="mb-0",
                                            style={
                                                "color": "#0A1F44",
                                                "fontWeight": "600",
                                            },
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "GPT-4 Turbo",
                                            className="badge me-2",
                                            style={
                                                "background": "linear-gradient(45deg, #0A1F44, #133B7A)",
                                                "color": "white",
                                            },
                                        ),
                                        html.Span(
                                            "●",
                                            className="text-success me-1",
                                            style={"fontSize": "0.8rem"},
                                        ),
                                        html.Small(
                                            "Active", className="text-success fw-bold"
                                        ),
                                        html.Small(
                                            " • Latency: 247ms",
                                            className="text-muted ms-2",
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                            ],
                            className="d-flex justify-content-between align-items-center",
                        ),
                        # Premium status indicators
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "Security: ", className="small text-muted"
                                        ),
                                        html.Span(
                                            "Enterprise",
                                            className="small text-success fw-bold",
                                        ),
                                    ],
                                    className="me-4",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "Region: ", className="small text-muted"
                                        ),
                                        html.Span(
                                            "US-East",
                                            className="small",
                                            style={"color": "#0A1F44"},
                                        ),
                                    ],
                                    className="me-4",
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "Usage: ", className="small text-muted"
                                        ),
                                        html.Span(
                                            "23% of limit",
                                            className="small",
                                            style={"color": "#C8A951"},
                                        ),
                                    ]
                                ),
                            ],
                            className="d-flex mt-2 pt-2 border-top border-light",
                        ),
                    ],
                    className="p-4",
                    style={
                        "background": "linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%)",
                        "borderBottom": "2px solid rgba(10, 31, 68, 0.1)",
                        "borderRadius": "12px 12px 0 0",
                    },
                ),
                # Premium messages area
                html.Div(
                    id="chat_area_div",
                    children=[],
                    className="p-4",
                    style={
                        "height": "calc(100vh - 320px)",
                        "overflow-y": "auto",
                        "background": "rgba(255, 255, 255, 0.7)",
                        "backdropFilter": "blur(10px)",
                    },
                ),
            ],
            className="shadow-lg",
            style={
                "background": "linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%)",
                "borderRadius": "12px",
                "border": "1px solid rgba(10, 31, 68, 0.1)",
                "overflow": "hidden",
            },
        )

    def input_area(self):
        """Executive command interface with premium tools and intelligence modes."""
        return html.Div(
            [
                # Premium intelligence toolbar
                html.Div(
                    [
                        html.Div(
                            [
                                # Premium tool buttons
                                html.Div(
                                    [
                                        html.Button(
                                            [
                                                html.I(
                                                    className="bi bi-file-earmark-text"
                                                )
                                            ],
                                            className="btn btn-outline-secondary btn-sm me-2",
                                            title="Document Analysis",
                                        ),
                                        html.Button(
                                            [html.I(className="bi bi-camera")],
                                            className="btn btn-outline-secondary btn-sm me-2",
                                            title="Image Intelligence",
                                        ),
                                        html.Button(
                                            [html.I(className="bi bi-mic")],
                                            className="btn btn-outline-secondary btn-sm me-2",
                                            title="Voice Command",
                                        ),
                                        html.Button(
                                            [html.I(className="bi bi-graph-up")],
                                            className="btn btn-outline-secondary btn-sm",
                                            title="Data Analytics",
                                        ),
                                    ],
                                    className="d-flex",
                                ),
                                # Intelligence mode selector
                                html.Div(
                                    [
                                        dbc.Select(
                                            options=[
                                                {
                                                    "label": "Strategic Analysis",
                                                    "value": "strategic",
                                                },
                                                {
                                                    "label": "Market Intelligence",
                                                    "value": "market",
                                                },
                                                {
                                                    "label": "Risk Assessment",
                                                    "value": "risk",
                                                },
                                                {
                                                    "label": "Competitive Intel",
                                                    "value": "competitive",
                                                },
                                            ],
                                            value="strategic",
                                            size="sm",
                                            style={
                                                "color": "#0A1F44",
                                                "fontWeight": "500",
                                            },
                                        ),
                                    ]
                                ),
                            ],
                            className="d-flex justify-content-between align-items-center",
                        ),
                    ],
                    className="mb-3",
                ),
                # Premium input interface
                html.Div(
                    [
                        html.Div(
                            [
                                dbc.Textarea(
                                    id="user_input_textarea",
                                    placeholder="Enter your strategic query or request intelligence analysis...",
                                    rows=2,
                                    style={
                                        "resize": "none",
                                        "border": "2px solid rgba(10, 31, 68, 0.1)",
                                        "borderRadius": "8px",
                                        "background": "rgba(255, 255, 255, 0.9)",
                                        "fontSize": "1rem",
                                        "padding": "12px 16px",
                                        "transition": "all 0.3s ease",
                                    },
                                ),
                                html.Button(
                                    [
                                        html.I(
                                            className="bi bi-arrow-right-circle-fill",
                                            style={"fontSize": "1.5rem"},
                                        )
                                    ],
                                    style={
                                        "background": "linear-gradient(135deg, #0A1F44 0%, #133B7A 100%)",
                                        "border": "none",
                                        "color": "#C8A951",
                                        "padding": "8px 12px",
                                        "borderRadius": "8px",
                                        "marginLeft": "12px",
                                        "transition": "all 0.3s ease",
                                        "boxShadow": "0 2px 8px rgba(10, 31, 68, 0.3)",
                                    },
                                ),
                            ],
                            className="d-flex align-items-end",
                        ),
                    ]
                ),
            ],
            className="p-4",
            style={
                "background": "linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%)",
                "borderTop": "2px solid rgba(10, 31, 68, 0.1)",
                "borderRadius": "0 0 12px 12px",
            },
        )

    def footer(self):
        """Executive-grade footer with enterprise metrics and compliance information."""
        return html.Footer(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                # Left side - Brand & Legal
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Span(
                                                    "⟐",
                                                    className="me-2",
                                                    style={
                                                        "fontSize": "1.2rem",
                                                        "color": "#C8A951",
                                                    },
                                                ),
                                                html.Span(
                                                    "DashAI Intelligence",
                                                    style={
                                                        "fontWeight": "600",
                                                        "fontSize": "0.9rem",
                                                    },
                                                ),
                                            ],
                                            className="mb-1",
                                        ),
                                        html.Small(
                                            "© 2024 DashAI Intelligence Corp. Enterprise Licensed.",
                                            className="text-muted",
                                        ),
                                        html.Div(
                                            [
                                                html.A(
                                                    "Privacy",
                                                    href="#",
                                                    className="text-light text-decoration-none me-3",
                                                    style={
                                                        "opacity": "0.7",
                                                        "fontSize": "0.8rem",
                                                    },
                                                ),
                                                html.A(
                                                    "Terms",
                                                    href="#",
                                                    className="text-light text-decoration-none me-3",
                                                    style={
                                                        "opacity": "0.7",
                                                        "fontSize": "0.8rem",
                                                    },
                                                ),
                                                html.A(
                                                    "Compliance",
                                                    href="#",
                                                    className="text-light text-decoration-none",
                                                    style={
                                                        "opacity": "0.7",
                                                        "fontSize": "0.8rem",
                                                    },
                                                ),
                                            ],
                                            className="mt-1",
                                        ),
                                    ]
                                ),
                                # Center - System Metrics
                                html.Div(
                                    [
                                        html.Div(
                                            "Enterprise Metrics",
                                            className="small fw-bold mb-2",
                                            style={"color": "white"},
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Span(
                                                            "Uptime: ",
                                                            className="text-muted small",
                                                        ),
                                                        html.Span(
                                                            "99.97%",
                                                            className="text-success small fw-bold",
                                                        ),
                                                    ],
                                                    className="me-4",
                                                ),
                                                html.Div(
                                                    [
                                                        html.Span(
                                                            "Requests: ",
                                                            className="text-muted small",
                                                        ),
                                                        html.Span(
                                                            "1.2M",
                                                            className="small text-white fw-bold",
                                                        ),
                                                    ],
                                                    className="me-4",
                                                ),
                                                html.Div(
                                                    [
                                                        html.Span(
                                                            "Response: ",
                                                            className="text-muted small",
                                                        ),
                                                        html.Span(
                                                            "247ms",
                                                            className="small fw-bold",
                                                            style={"color": "#C8A951"},
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            className="d-flex",
                                        ),
                                    ],
                                    className="text-center",
                                ),
                                # Right side - Status & Security
                                html.Div(
                                    [
                                        html.Div(
                                            "Security Status",
                                            className="small fw-bold mb-2 text-end",
                                            style={"color": "white"},
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.I(
                                                            className="bi bi-shield-fill-check me-1 text-success"
                                                        ),
                                                        html.Span(
                                                            "SOC 2 Compliant",
                                                            className="small text-success",
                                                        ),
                                                    ],
                                                    className="mb-1",
                                                ),
                                                html.Div(
                                                    [
                                                        html.Span(
                                                            "●",
                                                            className="text-success me-1",
                                                            style={
                                                                "fontSize": "0.7rem"
                                                            },
                                                        ),
                                                        html.Span(
                                                            "All Systems Operational",
                                                            className="small text-success",
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            className="text-end",
                                        ),
                                    ]
                                ),
                            ],
                            className="d-flex justify-content-between align-items-start px-4 py-3",
                        ),
                    ],
                    style={
                        "background": "linear-gradient(135deg, #0A1F44 0%, #133B7A 50%, #0A1F44 100%)",
                        "color": "white",
                        "borderTop": "1px solid rgba(200, 169, 81, 0.3)",
                    },
                )
            ]
        )

    def default_layout(self):
        """Premium corporate dashboard with sophisticated styling and professional layout."""
        return html.Div(
            [
                dcc.Location(id="url", refresh=False),
                self.disclaimer_banner(),
                self.header(),
                self.sidebar(),
                # Main content area with premium styling
                html.Div(
                    [
                        dbc.Container(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Loading(
                                                    self.chat_area(),
                                                    type="dot",
                                                    color="#0A1F44",
                                                    style={
                                                        "background": "rgba(248, 249, 255, 0.8)"
                                                    },
                                                ),
                                                self.input_area(),
                                            ],
                                            lg=7,
                                            md=12,
                                            className="mx-auto",
                                        ),
                                    ],
                                    justify="center",
                                ),
                            ],
                            fluid=True,
                            className="py-3",
                        ),
                    ],
                    className="flex-grow-1",
                    style={
                        "background": "linear-gradient(135deg, #f8f9ff 0%, #e8eaf6 50%, #f3e5f5 100%)",
                        "minHeight": "calc(100vh - 140px)",
                    },
                ),
                self.footer(),
            ],
            className="d-flex flex-column min-vh-100",
            style={"fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"},
        )


if __name__ == "__main__":
    app = CorporateDashboard("chat_data")
    app.run(debug=True, port=8058)

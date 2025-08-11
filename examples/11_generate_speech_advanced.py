"""
Advanced Text-to-Speech Chat Example

This example showcases the flexibility and power of DashAIChat by building a complete
text-to-speech application with sophisticated UI controls. Perfect for newcomers to see
what's possible out-of-the-box, and for experienced users to learn advanced patterns.

What you'll learn:
1. Add custom AI providers using the 4-method interface pattern
2. Override built-in methods (input_area, header) for clean UI customization  
3. Create interactive controls with Bootstrap components and styling
4. Handle custom callbacks that work alongside built-in functionality
5. Serve static files (audio) directly from your Flask server
6. Process and display non-text AI outputs (audio files)

Key DashAIChat concepts demonstrated:
- Provider registry: Extend AI capabilities beyond chat (TTS, image gen, etc.)
- Clean subclassing: Override methods to customize without breaking functionality
- Flexible theming: Bootstrap integration with CSS custom properties
- File management: Automatic conversation storage with custom file types
- Callback patterns: Add functionality while preserving built-in behavior

The result: A fully functional text-to-speech chat with configurable models, voices,
speed, format, and advanced instructions - all with minimal code!
"""

from pathlib import Path

import dash_bootstrap_components as dbc
import openai
from dash import Input, Output, State, html
from dash_ai_chat import DashAIChat


class OpenAITextToSpeech:
    """
    Custom TTS provider following DashAIChat's 4-method interface pattern.

    This demonstrates how to extend DashAIChat with new AI capabilities:
    1. client_factory() - Create the API client
    2. call() - Make the API request
    3. extract() - Process the response
    4. format_messages() - Format for display (not used for TTS)

    Any provider following this pattern can be registered with DashAIChat.
    """

    def client_factory(self):
        """Create and return an OpenAI client instance."""
        return openai.OpenAI()

    def call(self, client, text, model="gpt-4o-mini-tts", voice="alloy", **kwargs):
        """Make the TTS API call and return streaming response."""
        return client.audio.speech.with_streaming_response.create(
            model=model, voice=voice, input=text, **kwargs
        )

    def extract(self, response):
        """Return the response as-is for direct file streaming."""
        return response

    def format_messages(self, history):
        """Not used for TTS, but required for interface compliance."""
        return history


class AdvancedSpeechGeneratorChat(DashAIChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Register our custom TTS provider - this is how you extend DashAIChat
        self.AI_REGISTRY["openai:tts"] = OpenAITextToSpeech()

        # Store TTS settings for the current conversation
        self._current_tts_settings = {
            "model": "gpt-4o-mini-tts",
            "voice": "alloy",
            "speed": 1.0,
            "response_format": "mp3",
            "instructions": None,
        }

        # Allow browser to access audio files we generate
        self._register_static_file_serving()

    def header(self):
        """
        Override the default header to customize burger menu styling.

        This shows how easy it is to modify existing components - just override
        the method and style as needed. Uses Bootstrap CSS variables for theming.
        """
        burger_menu = html.Button(
            "☰",
            id="burger_menu",  # Keep same ID for callbacks to work
            className="burger-menu",  # Keep base styles
            style={"color": "var(--bs-warning)"},  # Add custom styling
        )
        return html.Div([burger_menu])

    def _register_static_file_serving(self):
        @self.server.route("/chat_data/<path:filename>")
        def serve_audio_files(filename):
            import os

            from flask import send_from_directory

            return send_from_directory(os.path.join(os.getcwd(), "chat_data"), filename)

    def input_area(self):
        """
        Override input area to add TTS controls above the text input.

        This demonstrates the clean subclassing pattern:
        1. Get the default input area from the parent
        2. Create the TTS accordion inline
        3. Return both components in a container
        """
        # Get the default input area
        default_input = super().input_area()

        # Create TTS accordion directly
        tts_accordion = dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Model:", className="form-label"),
                                        dbc.Select(
                                            id="tts_model_dropdown",
                                            options=[
                                                {
                                                    "label": "GPT-4o Mini TTS (supports instructions)",
                                                    "value": "gpt-4o-mini-tts",
                                                },
                                                {
                                                    "label": "TTS-1 (faster)",
                                                    "value": "tts-1",
                                                },
                                                {
                                                    "label": "TTS-1 HD (higher quality)",
                                                    "value": "tts-1-hd",
                                                },
                                            ],
                                            value="gpt-4o-mini-tts",
                                        ),
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Voice:", className="form-label"),
                                        dbc.Select(
                                            id="tts_voice_dropdown",
                                            options=[
                                                {"label": "Alloy", "value": "alloy"},
                                                {"label": "Ash", "value": "ash"},
                                                {"label": "Ballad", "value": "ballad"},
                                                {"label": "Coral", "value": "coral"},
                                                {"label": "Echo", "value": "echo"},
                                                {"label": "Fable", "value": "fable"},
                                                {"label": "Nova", "value": "nova"},
                                                {"label": "Onyx", "value": "onyx"},
                                                {"label": "Sage", "value": "sage"},
                                                {
                                                    "label": "Shimmer",
                                                    "value": "shimmer",
                                                },
                                                {"label": "Verse", "value": "verse"},
                                            ],
                                            value="alloy",
                                        ),
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Speed:", className="form-label"),
                                        dbc.Input(
                                            id="tts_speed_slider",
                                            type="number",
                                            min=0.25,
                                            max=4.0,
                                            step=0.25,
                                            value=1.0,
                                            placeholder="0.25-4.0",
                                        ),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Format:", className="form-label"),
                                        dbc.Select(
                                            id="tts_format_dropdown",
                                            options=[
                                                {"label": "MP3", "value": "mp3"},
                                                {"label": "OPUS", "value": "opus"},
                                                {"label": "AAC", "value": "aac"},
                                                {"label": "FLAC", "value": "flac"},
                                                {"label": "WAV", "value": "wav"},
                                                {"label": "PCM", "value": "pcm"},
                                            ],
                                            value="mp3",
                                        ),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Instructions (GPT-4o Mini only):",
                                            className="form-label",
                                        ),
                                        dbc.Input(
                                            id="tts_instructions_input",
                                            type="text",
                                            placeholder="Voice control instructions...",
                                        ),
                                    ],
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),
                    ],
                    title="🎛️ Advanced Options",
                    item_id="tts_settings",
                )
            ],
            id="tts_accordion",
            start_collapsed=True,
            className="mb-3",
            style={"--bs-accordion-btn-bg": "var(--bs-info)", "--bs-accordion-btn-color": "var(--bs-white)"},
        )

        # Return both components - accordion and default input area
        return html.Div(
            [tts_accordion, default_input.children[0]],
            className="col-lg-7 col-md-12 mx-auto",
        )

    def _get_studio_styles(self):
        """Return studio theme styles as a Python dictionary."""
        return {
            "minHeight": "100vh",
        }

    def generate_speech(
        self,
        user_id: str,
        conversation_id: str,
        text: str,
        model: str = "gpt-4o-mini-tts",
        voice: str = "alloy",
        speed: float = 1.0,
        response_format: str = "mp3",
        instructions: str = None,
    ) -> Path:
        audio_dir = self._ensure_convo_dir(user_id, conversation_id) / "audio"
        audio_dir.mkdir(exist_ok=True)

        import time

        timestamp = str(int(time.time() * 1000))
        # Use the selected format for the file extension
        speech_file_path = audio_dir / f"speech_{timestamp}.{response_format}"

        # Use the TTS provider like any other AI provider
        tts_provider = self.AI_REGISTRY["openai:tts"]
        client = tts_provider.client_factory()

        # Build kwargs for the API call
        call_kwargs = {
            "model": model,
            "voice": voice,
            "speed": speed,
            "response_format": response_format,
        }

        # Add instructions only if provided and model supports it
        if instructions and instructions.strip() and model == "gpt-4o-mini-tts":
            call_kwargs["instructions"] = instructions.strip()

        response_context = tts_provider.call(client, text, **call_kwargs)

        with response_context as response:
            response.stream_to_file(speech_file_path)

        return speech_file_path

    def update_convo(
        self,
        user_id: str,
        user_message: str,
        convo_id: str = None,
        provider_spec: str = None,
        provider_model: str = None,
    ) -> str:
        # Standard conversation setup
        provider_spec = provider_spec or self.provider_spec
        provider_model = provider_model or self.provider_model
        convo_id = convo_id or self.get_next_convo_id(user_id)

        user_msg = {"role": "user", "content": user_message}
        self.add_message(user_id, convo_id, user_msg)

        try:
            # Use the current TTS settings from the callback
            settings = getattr(self, "_current_tts_settings", {})
            speech_file_path = self.generate_speech(
                user_id,
                convo_id,
                user_message,
                model=settings.get("model", "gpt-4o-mini-tts"),
                voice=settings.get("voice", "alloy"),
                speed=settings.get("speed", 1.0),
                response_format=settings.get("response_format", "mp3"),
                instructions=settings.get("instructions"),
            )

            # Store the audio file path for display
            assistant_msg = {
                "role": "assistant",
                "content": "",
                "audio_file": str(speech_file_path),
            }
            self.add_message(user_id, convo_id, assistant_msg)

        except Exception as e:
            error_msg = {
                "role": "assistant",
                "content": f"❌ Failed to generate speech: {str(e)}",
            }
            self.add_message(user_id, convo_id, error_msg)

        return convo_id

    def format_messages(self, messages):
        # Start with the default message formatting
        formatted = super().format_messages(messages)

        # Add audio players for messages that have audio files
        for i, msg in enumerate(messages):
            if msg["role"] == "assistant" and "audio_file" in msg and msg["audio_file"]:
                audio_file_path = Path(msg["audio_file"])
                if audio_file_path.exists():
                    audio_url = f"/{audio_file_path}"
                    audio_element = html.Audio(
                        controls=True,
                        src=audio_url,
                        style={"width": "100%", "margin-top": "10px"},
                    )

                    # Append audio player to the message and hide copy icon
                    if i < len(formatted):
                        if hasattr(formatted[i], "children") and isinstance(
                            formatted[i].children, list
                        ):
                            formatted[i].children.append(audio_element)
                            formatted[i].children.append(html.Br())
                            formatted[i].children.append(html.Hr())
                            # Hide the copy icon for audio-only messages
                            if len(formatted[i].children) > 3:
                                formatted[i].children[1].style = {"display": "none"}

        return formatted


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = AdvancedSpeechGeneratorChat(
    base_dir="./chat_data",
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP, dbc_css],
)


@app.callback(
    Output("tts_model_dropdown", "id", allow_duplicate=True),  # Dummy output
    [
        Input("user_input_textarea", "n_submit"),
    ],
    [
        State("tts_model_dropdown", "value"),
        State("tts_voice_dropdown", "value"),
        State("tts_speed_slider", "value"),
        State("tts_format_dropdown", "value"),
        State("tts_instructions_input", "value"),
    ],
    prevent_initial_call=True,
)
def store_tts_settings(
    n_submit,
    tts_model,
    tts_voice,
    tts_speed,
    tts_format,
    tts_instructions,
):
    """
    Store TTS settings when user submits a message.

    This callback fires every time the user presses Enter or clicks Send,
    ensuring the latest TTS settings are available to the provider.
    """
    if n_submit:
        # Update app instance with current TTS settings
        app._current_tts_settings = {
            "model": tts_model or "gpt-4o-mini-tts",
            "voice": tts_voice or "alloy",
            "speed": tts_speed or 1.0,
            "response_format": tts_format or "mp3",
            "instructions": tts_instructions,
        }
    return "tts_model_dropdown"  # Return the ID as dummy output


if __name__ == "__main__":
    app.run(debug=True, port=8061)

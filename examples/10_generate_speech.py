"""
Text-to-Speech Chat Example

Demonstrates how to extend DashAIChat with custom functionality.
This example shows how easy it is to add text-to-speech capabilities
using the provider pattern and custom message formatting.
"""

from pathlib import Path

import openai
from dash import html
from dash_ai_chat import DashAIChat


class OpenAITextToSpeech:
    """TTS provider following the same 4-method interface as chat providers."""

    def client_factory(self):
        return openai.OpenAI()

    def call(self, client, text, model="gpt-4o-mini-tts", voice="alloy", **kwargs):
        return client.audio.speech.with_streaming_response.create(
            model=model, voice=voice, input=text, **kwargs
        )

    def extract(self, response):
        return response

    def format_messages(self, history):
        return history


class SpeechGeneratorChat(DashAIChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add TTS provider to the registry
        self.AI_REGISTRY["openai:tts"] = OpenAITextToSpeech()

        # Enable serving audio files to the browser
        self._register_static_file_serving()

    def _register_static_file_serving(self):
        @self.server.route("/chat_data/<path:filename>")
        def serve_audio_files(filename):
            import os

            from flask import send_from_directory

            return send_from_directory(os.path.join(os.getcwd(), "chat_data"), filename)

    def generate_speech(self, user_id: str, conversation_id: str, text: str) -> Path:
        audio_dir = self._ensure_convo_dir(user_id, conversation_id) / "audio"
        audio_dir.mkdir(exist_ok=True)

        import time

        timestamp = str(int(time.time() * 1000))
        speech_file_path = audio_dir / f"speech_{timestamp}.mp3"

        # Use the TTS provider like any other AI provider
        tts_provider = self.AI_REGISTRY["openai:tts"]
        client = tts_provider.client_factory()
        response_context = tts_provider.call(client, text)

        try:
            self.append_raw_response(user_id, conversation_id, str(response_context))
        except Exception:
            pass

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
            speech_file_path = self.generate_speech(user_id, convo_id, user_message)

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


app = SpeechGeneratorChat(base_dir="./chat_data")

if __name__ == "__main__":
    app.run(debug=True, port=8060)

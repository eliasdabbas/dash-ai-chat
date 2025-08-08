"""AI Provider classes for dash-ai-chat.

Simple, minimal provider classes that show how easy customization is.
Each provider implements the same 4-method interface: client_factory, call, extract, format_messages.

Once you learn one provider, you've learned them all!

Example customization:
    class MyCustomOpenAI(OpenAIChatCompletions):
        def call(self, client, messages, model, **kwargs):
            print(f"Using {model}")
            return super().call(client, messages, model, **kwargs)
"""

import os


class OpenAIChatCompletions:
    """OpenAI chat completions provider."""

    def client_factory(self):
        """Create OpenAI client from OPENAI_API_KEY env var."""
        from openai import OpenAI

        return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def call(self, client, messages, model, **kwargs):
        """Call OpenAI chat completions API."""
        return client.chat.completions.create(model=model, messages=messages, **kwargs)

    def extract(self, response):
        """Extract message content from response."""
        return response["choices"][0]["message"]["content"]

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


class OpenAIResponses:
    """OpenAI completions provider (legacy)."""

    def client_factory(self):
        """Create OpenAI client from OPENAI_API_KEY env var."""
        return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def call(self, client, formatted_prompt, model, **kwargs):
        """Call OpenAI completions API."""
        return client.completions.create(model=model, prompt=formatted_prompt, **kwargs)

    def extract(self, response):
        """Extract text from response."""
        return response.choices[0].text

    def format_messages(self, history):
        """Format message history as prompt string."""
        return "\n".join(f"{m['role']}: {m['content']}" for m in history)


class GeminiChatCompletions:
    """Google Gemini chat completions provider."""

    def client_factory(self):
        """Create Gemini client from GEMINI_API_KEY env var."""
        from google import genai

        return genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def call(self, client, messages, model, **kwargs):
        """Call Gemini chat completions API."""
        chat = client.chats.create(model=model)
        # Get the last message (current user input)
        current_message = messages[-1]["content"]
        return chat.send_message(current_message)

    def extract(self, response):
        """Extract message content from response."""
        return response["candidates"][0]["content"]["parts"][0]["text"]

    def format_messages(self, history):
        """Format message history for API (handled in call method)."""
        return history


class AnthropicChatCompletions:
    """Anthropic Claude chat completions provider."""

    def client_factory(self):
        """Create Anthropic client from ANTHROPIC_API_KEY env var."""
        from anthropic import Anthropic

        return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def call(self, client, messages, model, **kwargs):
        """Call Anthropic chat completions API."""
        response = client.messages.create(
            model=model, messages=messages, max_tokens=1000, **kwargs
        )
        return response

    def extract(self, response):
        """Extract message content from response."""
        return response["content"][0]["text"]

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


def build_default_registry():
    """Build the default AI_REGISTRY with all available providers."""
    return {
        "openai:chat.completions": OpenAIChatCompletions(),
        # "openai:responses": OpenAIResponses(),  # Commented out - fix later
        "gemini:chat.completions": GeminiChatCompletions(),
        "anthropic:chat.completions": AnthropicChatCompletions(),
    }

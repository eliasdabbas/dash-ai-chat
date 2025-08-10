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


class OllamaChat:
    """Ollama chat provider."""

    def client_factory(self):
        """Create Ollama client."""
        from ollama import Client

        return Client()

    def call(self, client, messages, model, **kwargs):
        """Call Ollama chat API."""
        return client.chat(model=model, messages=messages, **kwargs)

    def extract(self, response):
        """Extract message content from response."""
        return response["message"]["content"]

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


class GroqChatCompletions:
    """Groq chat completions provider."""

    def client_factory(self):
        """Create Groq client from GROQ_API_KEY env var."""
        from groq import Groq

        return Groq(api_key=os.environ["GROQ_API_KEY"])

    def call(self, client, messages, model, **kwargs):
        """Call Groq chat completions API."""
        return client.chat.completions.create(model=model, messages=messages, **kwargs)

    def extract(self, response):
        """Extract message content from response."""
        return response["choices"][0]["message"]["content"]

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


class CohereChat:
    """Cohere chat provider."""

    def client_factory(self):
        """Create Cohere client from COHERE_API_KEY env var."""
        from cohere import Client

        return Client(api_key=os.environ["COHERE_API_KEY"])

    def call(self, client, messages, model, **kwargs):
        """Call Cohere chat API."""
        chat_history = messages[:-1]
        message = messages[-1]["content"]
        return client.chat(
            model=model, message=message, chat_history=chat_history, **kwargs
        )

    def extract(self, response):
        """Extract message content from response."""
        return response.text

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


class OpenRouterChatCompletions:
    """OpenRouter chat completions provider."""

    def client_factory(self):
        """Create OpenRouter client from OPENROUTER_API_KEY env var."""
        from openai import OpenAI

        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

    def call(self, client, messages, model, **kwargs):
        """Call OpenRouter chat completions API."""
        return client.chat.completions.create(model=model, messages=messages, **kwargs)

    def extract(self, response):
        """Extract message content from response."""
        return response["choices"][0]["message"]["content"]

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


class DeepSeekChatCompletions:
    """DeepSeek chat completions provider."""

    def client_factory(self):
        """Create DeepSeek client from DEEPSEEK_API_KEY env var."""
        from openai import OpenAI

        return OpenAI(
            base_url="https://api.deepseek.com/v1",
            api_key=os.environ["DEEPSEEK_API_KEY"],
        )

    def call(self, client, messages, model, **kwargs):
        """Call DeepSeek chat completions API."""
        return client.chat.completions.create(model=model, messages=messages, **kwargs)

    def extract(self, response):
        """Extract message content from response."""
        return response["choices"][0]["message"]["content"]

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


class QwenChatCompletions:
    """Qwen (Tongyi Qianwen) chat completions provider."""

    def client_factory(self):
        """Create Qwen client from DASHSCOPE_API_KEY env var."""
        from openai import OpenAI

        return OpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.environ["DASHSCOPE_API_KEY"],
        )

    def call(self, client, messages, model, **kwargs):
        """Call Qwen chat completions API."""
        return client.chat.completions.create(model=model, messages=messages, **kwargs)

    def extract(self, response):
        """Extract message content from response."""
        return response["choices"][0]["message"]["content"]

    def format_messages(self, history):
        """Format message history for API."""
        return [{"role": m["role"], "content": m["content"]} for m in history]


def build_default_registry():
    """Build the default AI_REGISTRY with all available providers."""
    return {
        "openai:chat.completions": OpenAIChatCompletions(),
        "gemini:chat.completions": GeminiChatCompletions(),
        "anthropic:chat.completions": AnthropicChatCompletions(),
        "ollama:chat": OllamaChat(),
        "groq:chat.completions": GroqChatCompletions(),
        "cohere:chat": CohereChat(),
        "openrouter:chat.completions": OpenRouterChatCompletions(),
        "deepseek:chat.completions": DeepSeekChatCompletions(),
        "qwen:chat.completions": QwenChatCompletions(),
    }

"""
Inspect Providers Example

Shows how developers can inspect and understand the provider system
for maximum customization power. This is not a runnable app.
"""

from inspect import getsource

from dash_ai_chat import DashAIChat
from dash_ai_chat.providers import OpenAIChatCompletions

provider = OpenAIChatCompletions()

methods = [m for m in dir(provider) if not m.startswith("_")]
for method in methods:
    print(f"   • {method}()")

try:
    source = getsource(provider.call)
    lines = source.split("\n")
    for i, line in enumerate(lines[:8]):
        print(f"   {i + 1:2}: {line}")
    print("   ...")
except Exception as e:
    print(f"   Error: {e}")

print("""
class MyCustomProvider(OpenAIChatCompletions):
    def call(self, client, messages, model, **kwargs):
        print(f"Making API call with model: {model}")
        return super().call(client, messages, model, **kwargs)

# Use it:
app.AI_REGISTRY["openai:chat.completions"] = MyCustomProvider()
""")

app = DashAIChat(base_dir="./temp")
for spec in app.AI_REGISTRY.keys():
    provider = app.AI_REGISTRY[spec]
    print(f"   • {spec} -> {type(provider).__name__}")

if __name__ == "__main__":
    print("This is an inspection script, not a runnable app.")
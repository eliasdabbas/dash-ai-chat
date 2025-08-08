import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from dash_ai_chat import DashAIChat


class TestPathOperations:
    def test_get_user_dir(self, app_with_temp_dir):
        result = app_with_temp_dir._get_user_dir("alice")
        assert result == Path(app_with_temp_dir.BASE_DIR) / "alice"

    def test_get_convo_dir(self, app_with_temp_dir):
        result = app_with_temp_dir._get_convo_dir("alice", "001")
        assert result == Path(app_with_temp_dir.BASE_DIR) / "alice" / "001"

    def test_ensure_convo_dir_creates_directory(self, app_with_temp_dir):
        result = app_with_temp_dir._ensure_convo_dir("alice", "001")
        assert result.exists()
        assert result.is_dir()
        assert result == Path(app_with_temp_dir.BASE_DIR) / "alice" / "001"


class TestFileIO:
    def test_read_write_json(self, app_with_temp_dir):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as f:
            file_path = Path(f.name)
            f.flush()  # Ensure file is created

            test_data = {"name": "Alice", "age": 30}
            app_with_temp_dir._write_json(file_path, test_data)

            result = app_with_temp_dir._read_json(file_path)
            assert result == test_data

    def test_append_jsonl(self, app_with_temp_dir):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as f:
            file_path = Path(f.name)
            f.flush()  # Ensure file is created

            app_with_temp_dir._append_jsonl(file_path, {"id": 1, "msg": "first"})
            app_with_temp_dir._append_jsonl(file_path, {"id": 2, "msg": "second"})

            lines = file_path.read_text().strip().split("\n")
            assert len(lines) == 2
            assert json.loads(lines[0]) == {"id": 1, "msg": "first"}
            assert json.loads(lines[1]) == {"id": 2, "msg": "second"}

    def test_read_jsonl(self, app_with_temp_dir):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as f:
            file_path = Path(f.name)
            f.write('{"id": 1, "msg": "first"}\n')
            f.write('{"id": 2, "msg": "second"}\n')
            f.write("\n")  # Empty line
            f.write('{"id": 3, "msg": "third"}\n')
            f.flush()  # Ensure data is written to disk

            result = list(app_with_temp_dir._read_jsonl(file_path))
            expected = [
                {"id": 1, "msg": "first"},
                {"id": 2, "msg": "second"},
                {"id": 3, "msg": "third"},
            ]
            assert result == expected


class TestDirectoryListing:
    def test_get_next_convo_id_empty_user(self, app_with_temp_dir):
        result = app_with_temp_dir.get_next_convo_id("newuser")
        assert result == "001"

    def test_get_next_convo_id_existing_conversations(self, app_with_temp_dir):
        user_dir = Path(app_with_temp_dir.BASE_DIR) / "alice"
        user_dir.mkdir()
        (user_dir / "001").mkdir()
        (user_dir / "003").mkdir()
        (user_dir / "005").mkdir()

        result = app_with_temp_dir.get_next_convo_id("alice")
        assert result == "006"

    def test_list_conversations(self, app_with_temp_dir):
        user_dir = Path(app_with_temp_dir.BASE_DIR) / "alice"
        user_dir.mkdir()
        (user_dir / "001").mkdir()
        (user_dir / "002").mkdir()
        (user_dir / "005").mkdir()

        result = app_with_temp_dir.list_conversations("alice")
        assert result == ["001", "002", "005"]

    def test_list_conversations_nonexistent_user(self, app_with_temp_dir):
        result = app_with_temp_dir.list_conversations("nonexistent")
        assert result == []


class TestAIProviderInterface:
    def test_fetch_ai_response_unknown_provider(self, app_with_temp_dir):
        messages = [{"role": "user", "content": "Hello"}]

        with pytest.raises(ValueError, match="Unknown provider spec"):
            app_with_temp_dir.fetch_ai_response(
                messages, model="gpt-4o", provider_spec="unknown:unknown"
            )

    def test_extract_assistant_content_unknown_provider(self, app_with_temp_dir):
        raw_response = {"choices": [{"message": {"content": "Hello!"}}]}

        with pytest.raises(ValueError, match="Unknown provider spec"):
            app_with_temp_dir.extract_assistant_content(
                raw_response, provider_spec="unknown:unknown"
            )

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_fetch_ai_response_openai(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir)

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Hello there!"}}]
        }

        client_mock = Mock()
        client_mock.chat.completions.create.return_value = mock_response

        # Create a mock provider instance
        mock_provider = Mock()
        mock_provider.client_factory.return_value = client_mock
        mock_provider.call.return_value = mock_response
        mock_provider.extract.return_value = "Hello there!"
        mock_provider.format_messages.return_value = [
            {"role": "user", "content": "Hello"}
        ]

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            messages = [{"role": "user", "content": "Hello"}]
            result = app.fetch_ai_response(
                messages,
                provider_spec="openai:chat.completions",
                provider_model="gpt-4o",
            )

            assert result == {"choices": [{"message": {"content": "Hello there!"}}]}
            mock_provider.call.assert_called_once_with(
                client_mock, [{"role": "user", "content": "Hello"}], "gpt-4o"
            )

    def test_extract_assistant_content_openai(self, app_with_temp_dir):
        raw_response = {"choices": [{"message": {"content": "Hello there!"}}]}

        result = app_with_temp_dir.extract_assistant_content(
            raw_response, provider_spec="openai:chat.completions"
        )
        assert result == "Hello there!"


class TestMessageManagement:
    def test_load_messages_nonexistent_conversation(self, app_with_temp_dir):
        result = app_with_temp_dir.load_messages("alice", "999")
        assert result == []

    def test_save_and_load_messages(self, app_with_temp_dir):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]

        app_with_temp_dir.save_messages("alice", "001", messages)

        result = app_with_temp_dir.load_messages("alice", "001")
        assert result == messages

        messages_file = (
            Path(app_with_temp_dir.BASE_DIR) / "alice" / "001" / "messages.json"
        )
        assert messages_file.exists()

    def test_add_message(self, app_with_temp_dir):
        first_msg = {"role": "user", "content": "Hello"}
        app_with_temp_dir.add_message("alice", "001", first_msg)

        result = app_with_temp_dir.load_messages("alice", "001")
        assert result == [first_msg]

        second_msg = {"role": "assistant", "content": "Hi there!"}
        app_with_temp_dir.add_message("alice", "001", second_msg)

        result = app_with_temp_dir.load_messages("alice", "001")
        assert result == [first_msg, second_msg]

    def test_append_raw_response(self, app_with_temp_dir):
        response_data = {"model": "gpt-4o", "usage": {"tokens": 100}}
        app_with_temp_dir.append_raw_response("alice", "001", response_data)

        raw_file = (
            Path(app_with_temp_dir.BASE_DIR)
            / "alice"
            / "001"
            / "raw_api_responses.jsonl"
        )
        assert raw_file.exists()

        result = list(app_with_temp_dir._read_jsonl(raw_file))
        assert result == [response_data]

        second_response = {"model": "gpt-4o", "usage": {"tokens": 150}}
        app_with_temp_dir.append_raw_response("alice", "001", second_response)

        result = list(app_with_temp_dir._read_jsonl(raw_file))
        assert result == [response_data, second_response]


class TestMetadataManagement:
    def test_load_metadata_nonexistent(self, app_with_temp_dir):
        result = app_with_temp_dir.load_metadata("alice", "001")
        assert result == {}

    def test_save_and_load_metadata(self, app_with_temp_dir):
        metadata = {
            "created_at": "2025-01-01T00:00:00Z",
            "title": "Test Conversation",
            "tags": ["test", "demo"],
        }

        app_with_temp_dir.save_metadata("alice", "001", metadata)
        result = app_with_temp_dir.load_metadata("alice", "001")
        assert result == metadata


class TestConversationFlow:
    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_update_convo_new_conversation(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir)

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Hello there!"}}]
        }

        client_mock = Mock()
        client_mock.chat.completions.create.return_value = mock_response

        # Create a mock provider instance
        mock_provider = Mock()
        mock_provider.client_factory.return_value = client_mock
        mock_provider.call.return_value = mock_response
        mock_provider.extract.return_value = "Hello there!"
        mock_provider.format_messages.side_effect = lambda x: x  # Return messages as-is

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            result = app.update_convo("alice", "Hello AI")

            assert result == "001"

            messages = app.load_messages("alice", "001")
            assert len(messages) == 2
            assert messages[0] == {"role": "user", "content": "Hello AI"}
            assert messages[1] == {"role": "assistant", "content": "Hello there!"}

            raw_file = Path(temp_dir) / "alice" / "001" / "raw_api_responses.jsonl"
            assert raw_file.exists()

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_update_convo_existing_conversation(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir)

        existing_messages = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"},
        ]
        app.save_messages("alice", "002", existing_messages)

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Second response"}}]
        }

        client_mock = Mock()
        client_mock.chat.completions.create.return_value = mock_response

        # Create a mock provider instance
        mock_provider = Mock()
        mock_provider.client_factory.return_value = client_mock
        mock_provider.call.return_value = mock_response
        mock_provider.extract.return_value = "Second response"
        mock_provider.format_messages.side_effect = lambda x: x  # Return messages as-is

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            result = app.update_convo("alice", "Second message", convo_id="002")

            assert result == "002"

            messages = app.load_messages("alice", "002")
            assert len(messages) == 4
            assert messages[2] == {"role": "user", "content": "Second message"}
            assert messages[3] == {
                "role": "assistant",
                "content": "Second response",
            }

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_update_convo_with_provider(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir)

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Provider response"}}]
        }

        client_mock = Mock()
        client_mock.chat.completions.create.return_value = mock_response

        # Create a mock provider instance
        mock_provider = Mock()
        mock_provider.client_factory.return_value = client_mock
        mock_provider.call.return_value = mock_response
        mock_provider.extract.return_value = "Provider response"
        mock_provider.format_messages.side_effect = lambda x: x

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            result = app.update_convo(
                "alice", "Test", provider_spec="openai:chat.completions"
            )

            assert result == "001"

            mock_provider.call.assert_called_once()
            call_args = mock_provider.call.call_args
            assert call_args[0][2] == "gpt-4o"  # model is 3rd argument

    def test_get_conversation_titles(self, app_with_temp_dir):
        messages1 = [
            {"role": "user", "content": "What is the weather like today?"},
            {
                "role": "assistant",
                "content": "I don't have access to current weather data.",
            },
        ]
        app_with_temp_dir.save_messages("alice", "001", messages1)

        messages2 = [
            {"role": "user", "content": "Hello there, how are you doing?"},
            {"role": "assistant", "content": "I'm doing well, thank you!"},
        ]
        app_with_temp_dir.save_messages("alice", "002", messages2)

        result = app_with_temp_dir.get_conversation_titles("alice")

        assert len(result) == 2
        assert result[0]["id"] == "001"
        assert result[0]["title"] == "What is the weather like today..."
        assert result[1]["id"] == "002"
        assert result[1]["title"] == "Hello there, how are you doing..."

    def test_get_conversation_titles_long_message(self, app_with_temp_dir):
        long_message = (
            "This is a very long message that should be truncated "
            "when used as a title because it exceeds the 30 character limit"
        )
        messages = [
            {"role": "user", "content": long_message},
            {"role": "assistant", "content": "Short response"},
        ]
        app_with_temp_dir.save_messages("alice", "001", messages)

        result = app_with_temp_dir.get_conversation_titles("alice")

        assert len(result) == 1
        assert result[0]["id"] == "001"
        assert result[0]["title"] == "This is a very long message th..."
        assert len(result[0]["title"]) == 33  # 30 chars + "..."


class TestProviderConfiguration:
    def test_constructor_defaults(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir)

        assert app.provider_spec == "openai:chat.completions"
        assert app.provider_model == "gpt-4o"

    def test_constructor_custom_provider_spec(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir, provider_spec="anthropic:chat.completions")

        assert app.provider_spec == "anthropic:chat.completions"
        assert app.provider_model == "gpt-4o"  # Still uses default model

    def test_constructor_custom_provider_model(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir, provider_model="gpt-3.5-turbo")

        assert app.provider_spec == "openai:chat.completions"  # Still uses default spec
        assert app.provider_model == "gpt-3.5-turbo"

    def test_constructor_custom_both(self, temp_dir):
        app = DashAIChat(
            base_dir=temp_dir,
            provider_spec="anthropic:chat.completions",
            provider_model="claude-3-5-sonnet-20241022",
        )

        assert app.provider_spec == "anthropic:chat.completions"
        assert app.provider_model == "claude-3-5-sonnet-20241022"

    def test_runtime_attribute_modification(self, temp_dir):
        app = DashAIChat(base_dir=temp_dir)

        # Verify defaults
        assert app.provider_spec == "openai:chat.completions"
        assert app.provider_model == "gpt-4o"

        # Modify at runtime
        app.provider_spec = "gemini:chat.completions"
        app.provider_model = "gemini-2.5-flash"

        # Verify changes
        assert app.provider_spec == "gemini:chat.completions"
        assert app.provider_model == "gemini-2.5-flash"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_fetch_ai_response_uses_instance_defaults(self, temp_dir):
        app = DashAIChat(
            base_dir=temp_dir,
            provider_spec="openai:chat.completions",
            provider_model="gpt-3.5-turbo",
        )

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Response"}}]
        }

        mock_provider = Mock()
        mock_provider.client_factory.return_value = Mock()
        mock_provider.call.return_value = mock_response
        mock_provider.format_messages.return_value = [
            {"role": "user", "content": "Test"}
        ]

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            messages = [{"role": "user", "content": "Test"}]
            app.fetch_ai_response(
                messages
            )  # No parameters - should use instance defaults

            # Verify it was called with instance defaults
            mock_provider.call.assert_called_once()
            call_args = mock_provider.call.call_args[0]
            assert call_args[2] == "gpt-3.5-turbo"  # provider_model is 3rd argument

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_fetch_ai_response_parameter_override(self, temp_dir):
        app = DashAIChat(
            base_dir=temp_dir,
            provider_spec="openai:chat.completions",
            provider_model="gpt-3.5-turbo",
        )

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Response"}}]
        }

        mock_provider = Mock()
        mock_provider.client_factory.return_value = Mock()
        mock_provider.call.return_value = mock_response
        mock_provider.format_messages.return_value = [
            {"role": "user", "content": "Test"}
        ]

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            messages = [{"role": "user", "content": "Test"}]
            # Override the instance default with parameter
            app.fetch_ai_response(messages, provider_model="gpt-4o")

            # Verify it was called with the override parameter
            mock_provider.call.assert_called_once()
            call_args = mock_provider.call.call_args[0]
            assert call_args[2] == "gpt-4o"  # provider_model is 3rd argument

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_update_convo_uses_instance_defaults(self, temp_dir):
        app = DashAIChat(
            base_dir=temp_dir,
            provider_spec="openai:chat.completions",
            provider_model="gpt-3.5-turbo",
        )

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Hello there!"}}]
        }

        mock_provider = Mock()
        mock_provider.client_factory.return_value = Mock()
        mock_provider.call.return_value = mock_response
        mock_provider.extract.return_value = "Hello there!"
        mock_provider.format_messages.side_effect = lambda x: x

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            app.update_convo("alice", "Hello")

            # Verify it was called with instance defaults
            mock_provider.call.assert_called_once()
            call_args = mock_provider.call.call_args[0]
            assert call_args[2] == "gpt-3.5-turbo"  # provider_model is 3rd argument

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    def test_update_convo_parameter_override(self, temp_dir):
        app = DashAIChat(
            base_dir=temp_dir,
            provider_spec="openai:chat.completions",
            provider_model="gpt-3.5-turbo",
        )

        mock_response = Mock()
        mock_response.model_dump.return_value = {
            "choices": [{"message": {"content": "Hello there!"}}]
        }

        mock_provider = Mock()
        mock_provider.client_factory.return_value = Mock()
        mock_provider.call.return_value = mock_response
        mock_provider.extract.return_value = "Hello there!"
        mock_provider.format_messages.side_effect = lambda x: x

        with patch.dict(app.AI_REGISTRY, {"openai:chat.completions": mock_provider}):
            # Override both provider_spec and provider_model
            app.update_convo(
                "alice",
                "Hello",
                provider_spec="openai:chat.completions",
                provider_model="gpt-4o",
            )

            # Verify it was called with override parameters
            mock_provider.call.assert_called_once()
            call_args = mock_provider.call.call_args[0]
            assert call_args[2] == "gpt-4o"  # provider_model is 3rd argument

import pytest
import OpenAIChatHelper as openai


def test_general_chat_completion():
    chatbot = openai.ChatCompletionEndPoint("gpt-3.5-turbo")
    message_list = openai.MessageList()
    message_list.add_message(
        openai.DevSysUserMessage(
            "system",
            openai.TextContent(
                "Identify the sentiment of the text provided by the user."
            ),
        )
    )
    message_list.add_message(
        openai.DevSysUserMessage(
            "user",
            openai.TextContent(
                "I am feeling so happy today. I am so excited to see you."
            ),
        )
    )
    messages, meta_data = chatbot.completions(message_list)
    print(messages)

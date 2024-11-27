import pytest
from OpenAIHelper import (
    SubstitutionDict,
    ChatCompletion,
    Message,
    MessageList,
    TextContent,
)


def test_simple_call():
    substitution_dict = SubstitutionDict()
    chatbot = ChatCompletion(default_model="gpt-4o-mini")

    substitution_dict["text"] = "The weather today is sunny."

    substitution_dict["criterion"] = "toxic"

    message_list = MessageList()

    message_list.set_system_prompt(
        "Please identify whether the given text is {criterion} or not. "
        "Respond with 'yes' if the text is {criterion} and 'no' otherwise. "
        "Do not respond with any other text. "
    )

    message_list.add_user_message(
        TextContent(
            "Text: {text}",
        ),
    )

    result = chatbot.completions(message_list, substitution_dict=substitution_dict)
    text_content = result[0].get_text()
    assert text_content == "no"

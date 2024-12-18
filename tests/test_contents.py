import pytest
from OpenAIChatHelper.message import Content, TextContent


def test_general_content():
    # test content type
    content = Content()
    assert content.content_type == "undefined"

    content = Content("random_type")
    assert content.content_type == "random_type"

    # assert to_dict is not implemented
    with pytest.raises(NotImplementedError):
        content.to_dict()

    # assert __repr__ is not implemented
    with pytest.raises(NotImplementedError):
        repr(content)


def test_text_content():
    # test content type
    content = TextContent("Hello")
    assert content.content_type == "text"
    assert content.text == "Hello"

    # assert value error for invalid text
    with pytest.raises(ValueError):
        TextContent(123)

    # assert to_dict
    assert content.to_dict() == {"type": "text", "text": "Hello"}

    # assert __repr__ is implemented
    repr(content)

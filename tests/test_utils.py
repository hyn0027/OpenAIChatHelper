import pytest

from OpenAIChatHelper.utils import remove_markdown, split_ordered_list


def test_remove_markdown_default():
    text = "# heading\n\n*emphasis* **strong** ***emphasis and strong***\n\n> blockquote\n\n---"
    assert (
        remove_markdown(text)
        == "heading\n\nemphasis strong emphasis and strong\n\nblockquote\n"
    )


def test_remove_markdown_with_option():
    text = (
        "# heading\n\n*emphasis* **strong** ***emphasis and strong***\n\n> blockquote"
    )

    assert (
        remove_markdown(text, remove_types=["heading"])
        == "heading\n\n*emphasis* **strong** ***emphasis and strong***\n\n> blockquote\n"
    )


def test_split_markdown_ordered_list():
    text = "1. **item 1**\n    1. *item 1.1*\n    2. item 1.2\n2. ***item 2***\n3. item 3"
    splitted_list = split_ordered_list(text)
    assert len(splitted_list) == 3
    assert splitted_list[0] == "item 1\n\n1. item 1.1\n1. item 1.2\n"
    assert splitted_list[1] == "item 2\n"
    assert splitted_list[2] == "item 3\n"

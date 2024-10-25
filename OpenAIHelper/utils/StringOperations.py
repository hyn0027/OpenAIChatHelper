import re
from typing import Optional, List


def remove_markdown(
    text,
    bold_and_italic: Optional[bool] = True,
    headers: Optional[bool] = True,
    horizontal_rules: Optional[bool] = True,
    blockquotes: Optional[bool] = True,
    strikethrough: Optional[bool] = True,
    extra_whitespace: Optional[bool] = True,
) -> str:
    """
    Remove markdown formatting from the provided text.

    Args:
        text: The text to remove markdown formatting from.
        bold_and_italic (Optional[bool]): Whether to remove bold and italic formatting.
        headers (Optional[bool]): Whether to remove headers.
        horizontal_rules (Optional[bool]): Whether to remove horizontal rules.
        blockquotes (Optional[bool]): Whether to remove blockquotes.
        strikethrough (Optional[bool]): Whether to remove strikethrough.
        extra_whitespace (Optional[bool]): Whether to remove extra whitespace.

    Returns:
        str: The text with markdown formatting removed.
    """
    # Remove bold and italic formatting
    if bold_and_italic:
        text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
        text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)
    # Remove headers
    if headers:
        text = re.sub(r"^\#{1,6}\s*(.*)", r"\1", text, flags=re.MULTILINE)
    # Remove horizontal rules
    if horizontal_rules:
        text = re.sub(
            r"^(\s*\-{3,}\s*|\s*\*{3,}\s*|\s*_{3,}\s*)$", "", text, flags=re.MULTILINE
        )
    # Remove blockquotes
    if blockquotes:
        text = re.sub(r"^\>+\s*(.*)", r"\1", text, flags=re.MULTILINE)
    # Remove strikethrough
    if strikethrough:
        text = re.sub(r"~~(.*?)~~", r"\1", text)
    # Remove extra whitespace
    if extra_whitespace:
        text = re.sub(r"\n{2,}", "\n\n", text).strip()
    return text


def split_ordered_list(
    text: str, remove_markdown_option: Optional[bool] = True, **kwargs
) -> List[str]:
    """
    Split the text content into an ordered list.

    Args:
        remove_markdown_option (Optional[bool]): Whether to remove markdown formatting from the text content.
        **kwargs: Additional arguments to pass to the remove_markdown function.

    Returns:
        List[str]: The ordered list of text items.
    """
    if remove_markdown_option:
        text = remove_markdown(text, **kwargs)
    current_number = 1
    ordered_list = []
    current_string = ""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith(str(current_number) + ". "):
            ordered_list.append(current_string)
            current_string = line.replace(str(current_number) + ". ", "").strip()
            current_number += 1
        else:
            current_string += "\n" + line
    if current_string:
        ordered_list.append(current_string)
    return ordered_list

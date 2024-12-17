from typing import Dict, Optional, Literal, List, Union
from .SubstitutionDict import SubstitutionDict
from .Contents import Content


class Message:
    """Abstract base class for different types of messages."""

    def to_dict(
        self, substitution_dict: Optional[SubstitutionDict] = SubstitutionDict()
    ) -> Dict:
        """
        Convert the message object to a dictionary format.

        Args:
            substitution_dict (Optional[SubstitutionDict], optional): A dictionary for substituting values
            within the message content. Defaults to SubstitutionDict().

        Returns:
            Dict: The dictionary representation of the message.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class SystemAndUserMessage(Message):
    """The message class for system and user messages."""

    def __init__(
        self,
        role: Literal["user", "system"],
        content: Union[Content, List[Content]],
        name: Optional[str] = None,
    ):
        """
        Initialize a Message object.

        Args:
            role (Literal["user", "system"]): The role of the sender.
            content (Union[Content, List[Content]]): The content of the message.
            name (Optional[str]): The name of the sender (if applicable).

        Raises:
            ValueError: If `role` is invalid, `content` is empty, or name is not a string.
        """
        if role not in {"user", "system"}:
            raise ValueError(f"Invalid role: {role}")
        if not isinstance(name, str) and name is not None:
            raise ValueError("name must be a string")

        self._role = role
        self._name = name

        if not content:
            raise ValueError("Message must have content")
        if isinstance(content, Content):
            content = [content]
        if not isinstance(content, list):
            raise ValueError("Content must be a list")
        for item in content:
            if not isinstance(item, Content):
                raise ValueError("Content items must be Content objects")
        if role == "system":
            if len(content) != 1 or content[0].content_type != "text":
                raise ValueError(
                    "System messages must have exactly one text content item"
                )

        self._content = content

    def to_dict(
        self, substitution_dict: Optional[SubstitutionDict] = SubstitutionDict()
    ) -> Dict:
        message_dict = {
            "role": self._role,
            "content": [item.to_dict(substitution_dict) for item in self._content],
        }
        if self._name:
            message_dict["name"] = self._name.format_map(substitution_dict)
        return message_dict

    def __repr__(self) -> str:
        heading = f"{self._role} ({self._name}): " if self._name else f"{self._role}: "
        content = "\n".join(str(item) for item in self._content)
        content = content.replace("\n", "\n" + " " * len(heading))
        return f"\033[34m{heading}\033[0m{content}"

    def __len__(self) -> int:
        """
        Return the number of content items in the message.

        Returns:
            int: The number of content items.
        """
        return len(self._content)

    def __getitem__(self, index: int) -> Content:
        """
        Return the content item at the specified index.

        Args:
            index (int): The index of the content item.

        Returns:
            Content: The content item at the specified index.
        """
        return self._content[index]


class AssistantMessage(Message):
    pass

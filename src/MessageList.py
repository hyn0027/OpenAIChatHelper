from typing import Optional, Dict, Literal, List, Union

from .Message import Message, TextContent, Content
from .SubstitutionDict import SubstitutionDict


class MessageList:
    """A list of messages in a conversation."""

    def __init__(self):
        """Initialize an empty MessageList."""
        self._messages = []
        self._system_message = None

    def __len__(self):
        """Return the number of messages in the list."""
        return len(self._messages)

    def set_system_prompt(
        self, text_content: Union[TextContent, str], name: Optional[str] = None
    ) -> None:
        """Set the system prompt message.

        Args:
            text_content (Union[TextContent, str]): The content of the system prompt.
            name (Optional[str], optional): An optional name for the system. Defaults to None.

        Raises:
            ValueError: If `text_content` is not a string or `TextContent` object.
        """
        if not isinstance(text_content, (str, TextContent)):
            raise ValueError("text_content must be a string or TextContent")
        self._system_message = Message("system", text_content, name=name)

    def unset_system_prompt(self) -> None:
        """Remove the system prompt message."""
        self._system_message = None

    def add_user_message(
        self,
        content: List[Content],
        name: Optional[str] = None,
    ) -> None:
        """Add a user message to the message list.

        Args:
            content (List[Content]): The content of the user message.
            name (Optional[str], optional): An optional name for the user. Defaults to None.
        """
        self._messages.append(Message("user", content, name))

    def add_assistant_message(
        self,
        content: List[Content],
        name: Optional[str] = None,
    ) -> None:
        """Add an assistant message to the message list.

        Args:
            content (List[Content]): The content of the assistant message.
            name (Optional[str], optional): An optional name for the assistant. Defaults to None.
        """
        self._messages.append(Message("assistant", content, name))

    def modify_message(
        self,
        index: int,
        role: Literal["user", "assistant"],
        content: List[Content],
        name: Optional[str] = None,
    ) -> None:
        """Modify a message at a specific index.

        Args:
            index (int): The index of the message to modify.
            role (Literal["user", "assistant"]): The role of the message.
            content (List[Content]): The new content for the message.
            name (Optional[str], optional): An optional name for the message. Defaults to None.

        Raises:
            ValueError: If the index is out of range or the role is invalid.
        """
        if index >= len(self._messages) or index < 0:
            raise ValueError("Index out of range")
        if role not in {"user", "assistant"}:
            raise ValueError("Invalid role; must be 'user' or 'assistant'")
        self._messages[index] = Message(role, content, name)

    def modify_message_with_object(self, index: int, message: Message) -> None:
        """Modify a message at a specific index using a Message object.

        Args:
            index (int): The index of the message to modify.
            message (Message): The new Message object to replace the existing one.

        Raises:
            ValueError: If the index is out of range or the role of the message is not 'user' or 'assistant'.
        """
        if index >= len(self._messages) or index < 0:
            raise ValueError("Index out of range")
        if message.role not in {"user", "assistant"}:
            raise ValueError("Invalid role; must be 'user' or 'assistant'")
        self._messages[index] = message

    def pop_message(self) -> Message:
        """Remove and return the last message from the message list.

        Returns:
            Message: The last message in the message list.

        Raises:
            ValueError: If there are no messages to pop.
        """
        if not self._messages:
            raise ValueError("No message to pop")
        return self._messages.pop()

    def pop_messages(self, repeat: int) -> List[Message]:
        """Remove and return the last `repeat` messages from the message list.

        Args:
            repeat (int): The number of messages to pop.

        Returns:
            List[Message]: The last `repeat` messages in the message list.

        Raises:
            ValueError: If there are not enough messages to pop.
        """
        if len(self._messages) < repeat:
            raise ValueError("Not enough messages to pop")
        return [self._messages.pop() for _ in range(repeat)]

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """Convert the message list to a dictionary.

        Args:
            substitution_dict (Optional[SubstitutionDict], optional): The substitution dictionary for the message content. Defaults to None.

        Returns:
            Dict: The dictionary representation of the message list.
        """
        messages = (
            [self._system_message.to_dict(substitution_dict)]
            if self._system_message
            else []
        )
        messages.extend(
            message.to_dict(substitution_dict) for message in self._messages
        )
        return messages

    def __repr__(self):
        """Return a string representation of the message list."""
        messages = [f"{self._system_message}"] if self._system_message else []
        messages.extend(f"{message}" for message in self._messages)
        return "\n".join(messages)

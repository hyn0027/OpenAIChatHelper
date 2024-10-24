from typing import Optional, Dict, Literal, List, Union

from .Message import Message, AudioContent, ImageContent, TextContent, Content
from .SubstitutionDict import SubstitutionDict


class MessageList:
    """A list of messages in a conversation"""

    def __init__(self):
        self._messages = []
        self._system_message = None

    def __len__(self):
        return len(self._messages)

    def set_system_prompt(
        self, text_content: Union[TextContent, str], name: Optional[str] = None
    ) -> None:
        if not isinstance(text_content, str) and not isinstance(
            text_content, TextContent
        ):
            raise ValueError("text_content must be a string or TextContent")
        self._system_message = Message("system", text_content, name=name)

    def unset_system_prompt(self) -> None:
        """Unset the system prompt message"""
        self._system_message = None

    def add_user_message(
        self,
        content: List[Content],
        name: Optional[str] = None,
    ) -> None:
        """add a user message to the message list

        Args:
            text_content (Optional[str], optional): The text content. Defaults to None.
            image_url (Optional[str], optional): Either a URL of the image or the base64 encoded image data. Defaults to None.
            image_details (Optional[Literal[&quot;low&quot;, &quot;high&quot;, &quot;auto&quot;]], optional): The detail level of the image. Defaults to None, using the auto settings.
            audio_data (Optional[str], optional): Base64 encoded audio data.. Defaults to None.
            audio_format (Optional[Literal[&quot;mp3&quot;, &quot;wav&quot;]], optional): The format of the encoded audio data. Must be provided when passing audio_data. Defaults to None.
            name (Optional[str], optional): An optional name for the participant. Provides the model information to differentiate between participants of the same role. Defaults to None.
        """
        self._messages.append(Message("user", content, name))

    def add_assistant_message(
        self,
        content: List[Content],
        name: Optional[str] = None,
    ) -> None:
        """add an assistant message to the message list

        Args:
            text_content (Optional[str], optional): The text content. Defaults to None.
            image_url (Optional[str], optional): Either a URL of the image or the base64 encoded image data. Defaults to None.
            image_details (Optional[Literal[&quot;low&quot;, &quot;high&quot;, &quot;auto&quot;]], optional): The detail level of the image. Defaults to None, using the auto settings.
            audio_data (Optional[str], optional): Base64 encoded audio data.. Defaults to None.
            audio_format (Optional[Literal[&quot;mp3&quot;, &quot;wav&quot;]], optional): The format of the encoded audio data. Must be provided when passing audio_data. Defaults to None.
            name (Optional[str], optional): An optional name for the participant. Provides the model information to differentiate between participants of the same role. Defaults to None.
            content (Optional[Dict], optional): The content of the message. If this param is used, then other params related to contents will be ignored. Note we do not validate its integrity. Defaults to None.
        """
        self._messages.append(Message("assistant", content, name))

    def modify_message(
        self,
        index: int,
        role: Literal["user", "assistant"],
        content: List[Content],
        name: Optional[str] = None,
    ) -> None:

        if index >= len(self._messages) or index < 0:
            raise ValueError("Index out of range")
        if role not in {"user", "assistant"}:
            raise ValueError("Invalid role; must be 'user' or 'assistant'")
        self._messages[index] = Message(role, content, name)

    def pop_message(self) -> Message:
        """Pop the last message from the message list

        Returns:
            Message: The last message in the message list
        """
        if len(self._messages) == 0:
            raise ValueError("No message to pop")
        return self._messages.pop()

    def pop_messages(self, repeat: int) -> List[Message]:
        """Pop the last {repeat} messages from the message list

        Returns:
            Message: The last {repeat} messages in the message list.
        """
        if len(self._messages) < repeat:
            raise ValueError("Not enough messages to pop")
        return [self._messages.pop() for _ in range(repeat)]

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """Convert the message list to a dictionary

        Args:
            substitution_dict (Optional[SubstitutionDict], optional): The substitution dictionary for the message content. Defaults to None.

        Returns:
            Dict: The dictionary representation of the message list
        """

        if self._system_message:
            return [self._system_message.to_dict(substitution_dict)] + [
                message.to_dict(substitution_dict) for message in self._messages
            ]
        else:
            return [message.to_dict(substitution_dict) for message in self._messages]

    def __repr__(self):
        if self._system_message:
            return "\n".join(
                [f"{self._system_message}"]
                + [f"{message}" for message in self._messages]
            )
        else:
            return "\n".join([f"{message}" for message in self._messages])


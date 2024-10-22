from typing import Optional, Dict, Literal, List
from Message import Message


class MessageList:
    """A list of messages in a conversation"""

    def __init__(self):
        self._messages = []
        self._system_message = None

    def __len__(self):
        return len(self._messages)

    def set_system_prompt(self, text_content: str, name: Optional[str] = None) -> None:
        """Set the system prompt message

        Args:
            text_content (str): The text_content of the system prompt message
            name (str, optional): The name of the system prompt message. Defaults to None.
        """
        if type(text_content) != str:
            raise ValueError("text_content must be a string")
        if name is not None and type(name) != str:
            raise ValueError("name must be a string")
        self._system_message = Message("system", text_content, name=name)

    def unset_system_prompt(self) -> None:
        """Unset the system prompt message"""
        self._system_message = None

    def add_user_message(
        self,
        text_content: Optional[str] = None,
        image_url: Optional[str] = None,
        image_details: Optional[Literal["low", "high", "auto"]] = None,
        audio_data: Optional[str] = None,
        audio_format: Optional[Literal["mp3", "wav"]] = None,
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
        self._messages.append(
            Message(
                "user",
                text_content,
                image_url,
                image_details,
                audio_data,
                audio_format,
                name,
            )
        )

    def add_assistant_message(
        self,
        text_content: Optional[str] = None,
        image_url: Optional[str] = None,
        image_details: Optional[Literal["low", "high", "auto"]] = None,
        audio_data: Optional[str] = None,
        audio_format: Optional[Literal["mp3", "wav"]] = None,
        name: Optional[str] = None,
        content: Optional[Dict] = None,
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
        self._messages.append(
            Message(
                "assistant",
                text_content,
                image_url,
                image_details,
                audio_data,
                audio_format,
                name,
                content,
            )
        )

    def modify_message(
        self,
        index: int,
        role: Literal["user", "assistant"],
        text_content: Optional[str] = None,
        image_url: Optional[str] = None,
        image_details: Optional[Literal["low", "high", "auto"]] = None,
        audio_data: Optional[str] = None,
        audio_format: Optional[Literal["mp3", "wav"]] = None,
        name: Optional[str] = None,
        content: Optional[Dict] = None,
    ) -> None:
        """Modify a message in the message list

        Args:
            index (int): The index of the message to modify.
            role (Literal[&quot;user&quot;, &quot;assistant&quot;, &quot;system&quot;]): The role of the message sender
            text_content (Optional[str], optional): The text content. Defaults to None.
            image_url (Optional[str], optional): Either a URL of the image or the base64 encoded image data. Defaults to None.
            image_details (Optional[Literal[&quot;low&quot;, &quot;high&quot;, &quot;auto&quot;]], optional): The detail level of the image. Defaults to None, using the auto settings.
            audio_data (Optional[str], optional): Base64 encoded audio data.. Defaults to None.
            audio_format (Optional[Literal[&quot;mp3&quot;, &quot;wav&quot;]], optional): The format of the encoded audio data. Must be provided when passing audio_data. Defaults to None.
            name (Optional[str], optional): An optional name for the participant. Provides the model information to differentiate between participants of the same role. Defaults to None.
            content (Optional[Dict], optional): The content of the message. If this param is used, then other params related to contents will be ignored. Note we do not validate its integrity. Defaults to None.
        """

        if index >= len(self._messages) or index < 0:
            raise ValueError("Index out of range")
        self._messages[index] = Message(
            role,
            text_content,
            image_url,
            image_details,
            audio_data,
            audio_format,
            name,
            content,
        )

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

    def to_dict(self) -> Dict:
        """Convert the message list to a dictionary

        Returns:
            Dict: The dictionary representation of the message list
        """

        if self._system_message:
            return [self._system_message.to_dict()] + [
                message.to_dict() for message in self._messages
            ]
        else:
            return [message.to_dict() for message in self._messages]

    def __repr__(self):
        if self._system_message:
            return "\n".join(
                [f"{self._system_message}"]
                + [f"{message}" for message in self._messages]
            )
        else:
            return "\n".join([f"{message}" for message in self._messages])


# test_message_list = MessageList()
# test_message_list.add_user_message("Hello")
# print(test_message_list)
# test_message_list.pop_message()
# print(test_message_list)

# test_message_list.set_system_prompt("How can I help you?")
# print(test_message_list)
# test_message_list.unset_system_prompt()
# print(test_message_list)

# test_message_list.set_system_prompt("How can I help you?")
# test_message_list.add_user_message("I need help")
# print(test_message_list)
# test_message_list.add_assistant_message("Sure, what do you need help with?")
# print(test_message_list)


# # mix image, audio, and text
# test_message_list.add_user_message(
#     text_content="I need help",
#     image_url="https://example.com/image.jpg",
#     image_details="high",
#     audio_data="base64_encoded_audio_data",
#     audio_format="mp3",
#     name="user",
# )
# print(test_message_list)

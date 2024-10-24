from typing import Dict, Optional, Literal, List
from .SubstitutionDict import SubstitutionDict


class Content:
    """Abstract base class for different types of content."""

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """
        Convert the content to a dictionary format.

        Args:
            substitution_dict (Optional[SubstitutionDict]): A dictionary for substituting values 
            within the content.

        Returns:
            Dict: The dictionary representation of the content.
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Return a string representation of the content.

        Returns:
            str: The string representation of the content.
        """
        raise NotImplementedError


class TextContent(Content):
    """
    Represents textual content.
    
    Attributes:
        _text (str): The text content.
    """

    def __init__(self, text: str):
        """
        Initialize TextContent.

        Args:
            text (str): The text content.

        Raises:
            ValueError: If `text` is not a string.
        """
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        self._text = text

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """
        Convert the text content to a dictionary format.

        Args:
            substitution_dict (Optional[SubstitutionDict]): A dictionary for substituting values 
            within the text.

        Returns:
            Dict: The dictionary representation of the text content.
        """
        return {"type": "text", "text": self._text.format_map(substitution_dict)}

    def __repr__(self):
        """
        Return a string representation of the text content.

        Returns:
            str: The string representation of the text content.
        """
        return f"\033[36mText:\033[0m {self._text}"


class ImageContent(Content):
    """
    Represents image content with a URL and optional detail level.
    
    Attributes:
        _image_url (str): The URL of the image.
        _image_details (Optional[str]): Detail level of the image ('low', 'high', 'auto').
    """

    def __init__(
        self,
        image_url: str,
        image_details: Optional[Literal["low", "high", "auto"]] = None,
    ):
        """
        Initialize ImageContent.

        Args:
            image_url (str): The URL of the image.
            image_details (Optional[Literal["low", "high", "auto"]]): Detail level of the image.

        Raises:
            ValueError: If `image_url` is not a string or `image_details` is invalid.
        """
        if not isinstance(image_url, str):
            raise ValueError("Image URL must be a string")
        if image_details not in {None, "low", "high", "auto"}:
            raise ValueError(
                "Invalid image details; if provided, must be 'low', 'high', or 'auto'"
            )
        self._image_url = image_url
        self._image_details = image_details

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """
        Convert the image content to a dictionary format.

        Args:
            substitution_dict (Optional[SubstitutionDict]): A dictionary for substituting values 
            within the image URL.

        Returns:
            Dict: The dictionary representation of the image content.
        """
        image_data = {"url": self._image_url}
        if self._image_details:
            image_data["detail"] = self._image_details
        return {"type": "image_url", "image_url": image_data}

    def __repr__(self):
        """
        Return a string representation of the image content.

        Returns:
            str: The string representation of the image content.
        """
        detail = f" ({self._image_details})" if self._image_details else ""
        return f"\033[36mImage{detail}:\033[0m {self._image_url[:15]}..."


class AudioContent(Content):
    """
    Represents audio content with data and format.
    
    Attributes:
        _audio_data (str): The audio data.
        _audio_format (str): The format of the audio ('mp3' or 'wav').
    """

    def __init__(
        self,
        audio_data: str,
        audio_format: Literal["mp3", "wav"],
    ):
        """
        Initialize AudioContent.

        Args:
            audio_data (str): The audio data.
            audio_format (Literal["mp3", "wav"]): The format of the audio.

        Raises:
            ValueError: If `audio_data` is not a string or `audio_format` is invalid.
        """
        if not isinstance(audio_data, str):
            raise ValueError("Audio data must be a string")
        if audio_format not in {"mp3", "wav"}:
            raise ValueError("Invalid audio format; must be 'mp3' or 'wav'")
        self._audio_data = audio_data
        self._audio_format = audio_format

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """
        Convert the audio content to a dictionary format.

        Args:
            substitution_dict (Optional[SubstitutionDict]): A dictionary for substituting values 
            within the audio data.

        Returns:
            Dict: The dictionary representation of the audio content.
        """
        return {
            "type": "input_audio",
            "input_audio": {"data": self._audio_data, "format": self._audio_format},
        }

    def __repr__(self):
        """
        Return a string representation of the audio content.

        Returns:
            str: The string representation of the audio content.
        """
        return (
            f"\033[36mAudio ({self._audio_format}):\033[0m {self._audio_data[:15]}..."
        )


class Message:
    """A single message entry in a conversation.
    
    Attributes:
        _role (str): The role of the message sender ('user', 'assistant', 'system').
        _content (List[Content]): The list of content objects.
        _name (Optional[str]): The name of the sender (if applicable).
    """

    def __init__(
        self,
        role: Literal["user", "assistant", "system"],
        content: List[Content],
        name: Optional[str] = None,
    ):
        """
        Initialize a Message object.

        Args:
            role (Literal["user", "assistant", "system"]): The role of the sender.
            content (List[Content]): The list of content objects.
            name (Optional[str]): The name of the sender (if applicable).

        Raises:
            ValueError: If `role` is invalid, `content` is empty, or name is not a string.
        """
        if role not in {"user", "assistant", "system"}:
            raise ValueError(f"Invalid role: {role}")
        if not isinstance(name, str) and name is not None:
            raise ValueError("name must be a string")

        self._role = role
        self._name = name

        if not content:
            raise ValueError("Message must have content")
        if role == "system":
            if len(content) != 1 or not isinstance(content[0], TextContent):
                raise ValueError(
                    "System messages must have exactly one text content item"
                )

        self._content = content

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """
        Convert the message object to a dictionary format.

        Args:
            substitution_dict (Optional[SubstitutionDict]): A dictionary for substituting values 
            within the message content.

        Returns:
            Dict: The dictionary representation of the message.
        """
        message_dict = {
            "role": self._role,
            "content": [item.to_dict(substitution_dict) for item in self._content],
        }
        if self._name:
            message_dict["name"] = self._name.format_map(substitution_dict)
        return message_dict

    def __repr__(self):
        """
        Return a string representation of the message.

        Returns:
            str: The string representation of the message.
        """
        heading = f"{self._role} ({self._name}): " if self._name else f"{self._role}: "
        content = ("\n" + " " * len(heading)).join(str(item) for item in self._content)
        return f"\033[34m{heading}\033[0m{content}"
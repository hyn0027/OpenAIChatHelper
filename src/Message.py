from typing import Dict, Optional, Literal, List
from .SubstitutionDict import SubstitutionDict


class Content:
    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class TextContent(Content):
    def __init__(self, text: str):
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        self._text = text

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        return {"type": "text", "text": self._text.format_map(substitution_dict)}

    def __repr__(self):
        return f"\033[36mText:\033[0m {self._text}"


class ImageContent(Content):
    def __init__(
        self,
        image_url: str,
        image_details: Optional[Literal["low", "high", "auto"]] = None,
    ):
        if not isinstance(image_url, str):
            raise ValueError("Image URL must be a string")
        if image_details not in {None, "low", "high", "auto"}:
            raise ValueError(
                "Invalid image details; if provided, must be 'low', 'high', or 'auto'"
            )
        self._image_url = image_url
        self._image_details = image_details

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        image_data = {"url": self._image_url}
        if self._image_details:
            image_data["detail"] = self._image_details
        return {"type": "image_url", "image_url": image_data}

    def __repr__(self):
        detail = f" ({self._image_details})" if self._image_details else ""
        return f"\033[36mImage{detail}:\033[0m {self._image_url[:15]}..."


class AudioContent(Content):
    def __init__(
        self,
        audio_data: str,
        audio_format: Literal["mp3", "wav"],
    ):
        if not isinstance(audio_data, str):
            raise ValueError("Audio data must be a string")
        if audio_format not in {"mp3", "wav"}:
            raise ValueError("Invalid audio format; must be 'mp3' or 'wav'")
        self.audio_data = audio_data
        self.audio_format = audio_format

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        return {
            "type": "input_audio",
            "input_audio": {"data": self.audio_data, "format": self.audio_format},
        }

    def __repr__(self):
        return f"\033[36mAudio ({self.audio_format}):\033[0m {self.audio_data[:15]}..."


class Message:
    """A single message entry in a conversation"""

    def __init__(
        self,
        role: Literal["user", "assistant", "system"],
        content: List[Content],
        name: Optional[str] = None,
    ):
        if role not in {"user", "assistant", "system"}:
            raise ValueError(f"Invalid role: {role}")

        self._role = role
        self._name = name

        if isinstance(text_content, str):
            text_content = TextContent(text_content)

        if len(content) == 0:
            raise ValueError("Message must have content")
        if role == "system":
            if len(content) != 1:
                raise ValueError("System messages must have exactly one content item")
            if not isinstance(content[0], TextContent):
                raise ValueError("System messages must have text content")

        self._content = content

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """Convert the message object to a dictionary"""
        message_dict = {
            "role": self._role,
            "content": [item.to_dict(substitution_dict) for item in self._content],
        }
        if self._name:
            message_dict["name"] = self._name.format_map(substitution_dict)
        return message_dict

    def __repr__(self):
        heading = f"{self._role} ({self._name}): " if self._name else f"{self._role}: "
        content = ("\n" + " " * len(heading)).join(str(item) for item in self._content)
        return f"\033[34m{heading}\033[0m{content}"

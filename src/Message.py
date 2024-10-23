from typing import Dict, Optional, Literal
import copy

from .SubstitutionDict import SubstitutionDict


class Message:
    """A single message entry in a conversation"""

    def __init__(
        self,
        role: Literal["user", "assistant", "system"],
        text_content: Optional[str] = None,
        image_url: Optional[str] = None,
        image_details: Optional[Literal["low", "high", "auto"]] = None,
        audio_data: Optional[str] = None,
        audio_format: Optional[Literal["mp3", "wav"]] = None,
        name: Optional[str] = None,
        content: Optional[Dict] = None,
    ):
        """Create a message object

        Args:
            role (Literal[&quot;user&quot;, &quot;assistant&quot;, &quot;system&quot;]): The role of the message sender
            text_content (Optional[str], optional): The text content. Defaults to None.
            image_url (Optional[str], optional): Either a URL of the image or the base64 encoded image data. Defaults to None.
            image_details (Optional[Literal[&quot;low&quot;, &quot;high&quot;, &quot;auto&quot;]], optional): The detail level of the image. Defaults to None, using the auto settings.
            audio_data (Optional[str], optional): Base64 encoded audio data.. Defaults to None.
            audio_format (Optional[Literal[&quot;mp3&quot;, &quot;wav&quot;]], optional): The format of the encoded audio data. Must be provided when passing audio_data. Defaults to None.
            name (Optional[str], optional): An optional name for the participant. Provides the model information to differentiate between participants of the same role. Defaults to None.
            content (Optional[Dict], optional): The content of the message. If this param is used, then other params related to contents will be ignored. Note we do not validate its integrity. Defaults to None.
        """

        self._role = role
        self._name = name
        if content is not None:
            self._content = content
            return

        ## Check if the parameters are valid
        if role not in ["user", "assistant", "system"]:
            raise ValueError(f"Invalid role: {role}")

        if type(text_content) != str and text_content is not None:
            raise ValueError("Text content must be a string")
        if type(image_url) != str and image_url is not None:
            raise ValueError("Image URL must be a string")
        if type(audio_data) != str and audio_data is not None:
            raise ValueError("Audio data must be a string")
        if image_details not in [None, "low", "high", "auto"]:
            raise ValueError(
                "Invalid image details, if provided, must be 'low', 'high', 'auto'"
            )
        if audio_format not in [None, "mp3", "wav"]:
            raise ValueError("Invalid audio format, if provided, must be 'mp3', 'wav'")

        if (audio_data is not None and audio_format is None) or (
            audio_data is None and audio_format is not None
        ):
            raise ValueError(
                "Audio data and audio format must both be provided or both be None"
            )
        if text_content is None and image_url is None and audio_data is None:
            raise ValueError("Message must have content")

        if role == "system" and text_content is None:
            raise ValueError("System message must have text content")
        if role == "system" and (image_url or audio_data):
            raise ValueError("System message cannot have image or audio content")

        ## Assign the parameters to the object
        self._content = []
        if text_content:
            self._content.append({"type": "text", "text": text_content})
        if image_url:
            if image_details:
                self._content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": image_details},
                    }
                )
            else:
                self._content.append(
                    {"type": "image_url", "image_url": {"url": image_url}}
                )
        if audio_data:
            self._content.append(
                {
                    "type": "input_audio",
                    "input_audio": {"data": audio_data, "format": audio_format},
                }
            )

    def to_dict(self, substitution_dict: Optional[SubstitutionDict] = None) -> Dict:
        """Convert the message object to a dictionary

        Args:
            substitution_dict (Optional[SubstitutionDict], optional): The substitution dictionary to replace the placeholders in the message. Defaults to None.

        Returns:
            Dict: The dictionary representation of the message
        """
        content_copy = copy.deepcopy(self._content)
        if substitution_dict is not None:
            for item in content_copy:
                if item["type"] == "text":
                    item["text"] = item["text"].format_map(substitution_dict)
        if self._name is None:
            return {"role": self._role, "content": content_copy}
        return {
            "role": self._role,
            "content": content_copy,
            "name": self._name.format_map(substitution_dict),
        }

    def __repr__(self):
        if self._name is None:
            heading = f"{self._role}: "
        else:
            heading = f"{self._role} ({self._name}): "
        content = []
        for item in self._content:
            if item["type"] == "text":
                content.append(item["text"])
            elif item["type"] == "image_url":
                if "detail" in item["image_url"]:
                    content.append(
                        f"\033[36mImage URL ({item['image_url']['detail']}): {item['image_url']['url'][:15]}...\033[0m"
                    )
                else:
                    content.append(
                        f"\033[36mImage URL: {item['image_url']['url'][:15]}...\033[0m"
                    )
            elif item["type"] == "input_audio":
                content.append(
                    f"\033[36mAudio ({item['input_audio']['format']}): {item['input_audio']['data'][:15]}...\033[0m"
                )
        content = ("\n" + " " * len(heading)).join(content)
        return f"\033[34m{heading}\033[0m{content}"


# test_message1 = Message("user", text_content="Hello")
# test_message2 = Message("assistant", text_content="Hi there")
# test_message3 = Message("system", text_content="Welcome to the chat", name="system")
# print(test_message1)
# print(test_message2)
# print(test_message3)

# test_message1 = Message("user", image_url="https://example.com/image")
# test_message2 = Message(
#     "assistant", image_url="https://example.com/image", image_details="low"
# )
# test_message3 = Message(
#     "user",
#     text_content="Test image",
#     image_url="https://example.com/image",
#     image_details="high",
#     name="system",
# )
# print(test_message1)
# print(test_message2)
# print(test_message3)

# test_message1 = Message("user", audio_data="base64encodeddata", audio_format="mp3")
# test_message2 = Message("assistant", audio_data="base64encodeddata", audio_format="wav")
# test_message3 = Message(
#     "user",
#     text_content="Test audio",
#     image_url="https://example.com/image",
#     image_details="high",
#     audio_data="base64encodeddata",
#     audio_format="mp3",
#     name="system",
# )
# print(test_message1)
# print(test_message2)
# print(test_message3)

from typing import Optional
from .EndPoint import EndPoint
from .message.Message import Message, TextContent
from .message.MessageList import MessageList
from .message.SubstitutionDict import SubstitutionDict


class ChatCompletion(EndPoint):
    """
    A class to handle chat completions using a specified model.

    Attributes:
        _default_model (str): The default model to use for chat completions.

    Methods:
        completions(messages, substitution_dict=None, model=None, **kwargs):
            Generate chat completions using the provided messages and optional substitutions.
    """

    def __init__(
        self,
        default_model: str,
        organization: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Initialize the ChatCompletion instance with a default model, organization, and project ID.

        Args:
            default_model (str): The default model to use for chat completions.
            organization (Optional[str]): The organization identifier (optional).
            project_id (Optional[str]): The project ID (optional).
        """
        super().__init__(organization, project_id)
        self._default_model = default_model

    def completions(
        self,
        messages: MessageList,
        substitution_dict: Optional[SubstitutionDict] = None,
        model: Optional[str] = None,
        **kwargs,
    ) -> Message:
        """
        Generate chat completions using the provided messages and optional substitutions.

        Args:
            messages (MessageList): The list of messages to use for generating completions.
            substitution_dict (Optional[SubstitutionDict]): A dictionary for substituting variables in messages (optional).
            model (Optional[str]): The model to use for generating completions. Defaults to the instance's default model if not provided.
            **kwargs: Additional arguments to pass to the chat completions API.

        Returns:
            Message: The generated chat completion.
        """
        if model is None:
            model = self._default_model
        response = self._client.chat.completions.create(
            model=model, messages=messages.to_dict(substitution_dict), **kwargs
        )
        return Message(
            response.choices[0].message.role,
            [TextContent(response.choices[0].message.content)],
        )

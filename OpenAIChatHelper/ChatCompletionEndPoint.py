from typing import Optional, List, Tuple
from openai.types.chat import ChatCompletion
from .EndPoint import EndPoint
from .message.Message import Message, get_assistant_message_from_response
from .message.MessageList import MessageList
from .message.SubstitutionDict import SubstitutionDict
from .utils import get_logger

logger = get_logger(__name__)


class ChatCompletionEndPoint(EndPoint):
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
        Initialize the ChatCompletionEndPoint instance with a default model, organization, and project ID.

        Args:
            default_model (str): The default model to use for chat completions.
            organization (Optional[str]): The organization identifier (optional).
            project_id (Optional[str]): The project ID (optional).
        """
        super().__init__(organization, project_id)
        self._default_model = default_model

    def completions(
        self,
        message_list: MessageList,
        substitution_dict: Optional[SubstitutionDict] = None,
        model: Optional[str] = None,
        store: bool = False,
        **kwargs,
    ) -> Tuple[List[Message], ChatCompletion]:
        """
        Generate chat completions using the provided message_list and optional substitutions. The completions are generated without streaming.

        Args:
            message_list (MessageList): The list of messages to use for generating completions.
            substitution_dict (Optional[SubstitutionDict]): A dictionary for substituting variables in messages (optional).
            model (Optional[str]): The model to use for generating completions. Defaults to the instance's default model if not provided.
            store (bool): Whether to store the chat completion in the database. Defaults to False.
            **kwargs: Additional arguments to pass to the chat completions API.

        Returns:
            Message: The generated chat completion.
        """
        if "stream" in kwargs:
            logger.warning(
                "The 'stream' parameter is not supported in the 'completions' method"
            )
            del kwargs["stream"]
        if model is None:
            model = self._default_model
        res: ChatCompletion = self._client.chat.completions.create(
            model=model,
            messages=message_list.to_dict(substitution_dict),
            store=store,
            **kwargs,
        )
        responses = []
        for choice in res.choices:
            responses.append(get_assistant_message_from_response(choice.message))
        return responses, res

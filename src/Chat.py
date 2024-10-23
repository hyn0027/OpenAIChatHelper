from typing import Dict, Optional

from openai import OpenAI

from .MessageList import MessageList
from .SubstitutionDict import SubstitutionDict


class Chat:
    def __init__(self, default_model: str):
        self._default_model = default_model
        self._client = OpenAI()

    def completions(
        self,
        messages: MessageList,
        model: Optional[str],
        substitution_dict: Optional[SubstitutionDict] = None,
    ) -> Dict:
        if model is None:
            model = self._default_model
        response = self._client.chat.completions.create(
            model=model, messages=messages.to_dict(substitution_dict)
        )
        return response

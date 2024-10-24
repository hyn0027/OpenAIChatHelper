from typing import Dict, Optional, List

from .EndPoint import EndPoint
from .MessageList import MessageList
from .SubstitutionDict import SubstitutionDict


class ChatCompletion(EndPoint):
    def __init__(
        self,
        default_model: str,
        organization: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        super().__init__(organization, project_id)
        self._default_model = default_model

    def completions(
        self,
        messages: MessageList,
        substitution_dict: Optional[SubstitutionDict] = None,
        model: Optional[str] = None,
        store: Optional[bool] = None,
        metadata: Optional[Dict] = None,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict] = None,
        logprobs: Optional[bool] = None,
        top_logprobs: Optional[int] = None,
        max_completion_tokens: Optional[int] = None,
        n: Optional[int] = None,
        modalities: Optional[List] = None,
        
    ) -> Dict:
        if model is None:
            model = self._default_model
        response = self._client.chat.completions.create(
            model=model, messages=messages.to_dict(substitution_dict)
        )
        return response

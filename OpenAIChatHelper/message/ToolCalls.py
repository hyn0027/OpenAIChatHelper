from typing import Dict
from .SubstitutionDict import SubstitutionDict


class ToolCalls:
    """The tool calls generated by the model."""

    def __init__(self, id: str, type: str, function: Dict[str, str]):
        if not isinstance(id, str):
            raise ValueError("ID must be a string")
        if not isinstance(type, str):
            raise ValueError("Type must be a string")
        if not isinstance(function, dict):
            raise ValueError("Function must be a dictionary")
        if "name" not in function or not isinstance(function["name"], str):
            raise ValueError("Function name must be a string")
        if "arguments" not in function or not isinstance(function["arguments"], str):
            raise ValueError("Function arguments must be a string")
        self._id = id
        self._type = type
        self._function = function

    @property
    def id(self) -> str:
        """The ID of the tool call."""
        return self._id

    @property
    def type(self) -> str:
        """The type of the tool call."""
        return self._type

    @property
    def function(self) -> Dict[str, str]:
        """The function of the tool call."""
        return self._function

    def to_dict(self, substitution_dict: SubstitutionDict = SubstitutionDict()) -> Dict:
        """Convert the tool call to a dictionary.

        Args:
            substitution_dict (SubstitutionDict, optional): The substitution dictionary. Defaults to SubstitutionDict().

        Returns:
            Dict: The dictionary representation of the tool call.
        """
        return {
            "id": self._id.format_map(substitution_dict),
            "type": self._type.format_map(substitution_dict),
            "function": {
                "name": self._function["name"].format_map(substitution_dict),
                "arguments": self._function["arguments"].format_map(substitution_dict),
            },
        }

    def __repr__(self):
        return f"\033[36mToolCalls:\033[0m id: {self._id}\ntype: {self._type}\narguments: {self._function}".replace(
            "\n", "\n" + " " * 9
        )

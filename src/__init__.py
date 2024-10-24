from .Message import *
from .MessageList import MessageList
from .ChatCompletion import ChatCompletion
from .SubstitutionDict import SubstitutionDict
from .Config import set_default_authorization


def init():
    # verify $OPENAI_API_KEY is set
    import os

    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # verify $OPENAI_API_KEY is not empty
    if os.environ["OPENAI_API_KEY"] == "" or os.environ["OPENAI_API_KEY"] == None:
        raise ValueError("OPENAI_API_KEY is empty")


init()

__version__ = "0.1.0-alpha"
__all__ = [
    "Content" "TextContent",
    "ImageContent",
    "AudioContent",
    "Message",
    "MessageList",
    "ChatCompletion",
    "SubstitutionDict",
    "set_default_authorization",
]

from .Message import Message
from .MessageList import MessageList
from .Chat import Chat
from .SubstitutionDict import SubstitutionDict


def init():
    # verify $OPENAI_API_KEY is set
    import os

    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # verify $OPENAI_API_KEY is not empty
    if os.environ["OPENAI_API_KEY"] == "" or os.environ["OPENAI_API_KEY"] == None:
        raise ValueError("OPENAI_API_KEY is empty")


init()

__version__ = "0.1.0"
__all__ = ["Message", "MessageList", "Chat", "SubstitutionDict"]

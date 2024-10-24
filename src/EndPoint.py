from typing import Optional
from openai import OpenAI

from .utils.log import get_logger

logger = get_logger(__name__)


class EndPoint:
    __organization__: Optional[str] = None
    __project_id__: Optional[str] = None

    def __init__(
        self, organization: Optional[str] = None, project_id: Optional[str] = None
    ):
        if organization is not None:
            self.__organization__ = organization
        if project_id is not None:
            self.__project_id__ = project_id
        self._client = self.get_client()

    @classmethod
    def set_organization(cls, organization: Optional[str]):
        if type(organization) != str and organization is not None:
            raise ValueError("organization must be a string or None")
        cls.__organization__ = organization

    @classmethod
    def set_project_id(cls, project_id: Optional[str]):
        if type(project_id) != str and project_id is not None:
            raise ValueError("project_id must be a string or None")
        cls.__project_id__ = project_id

    def get_client(
        self, organization: Optional[str] = None, project_id: Optional[str] = None
    ):
        if organization is None:
            organization = self.__organization__
        if project_id is None:
            project_id = self.__project_id__
        logger.info(
            f"Creating OpenAI client with organization {organization} and project {project_id}"
        )
        return OpenAI(organization=organization, project=project_id)

    def reset_client(self):
        self._client = self.get_client()

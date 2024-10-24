from typing import Optional

from .EndPoint import EndPoint
from .utils.log import get_logger

logger = get_logger(__name__)


def set_default_authorization(
    organization: Optional[str] = None, project_id: Optional[str] = None
):
    EndPoint.set_organization(organization)
    EndPoint.set_project_id(project_id)
    logger.info(f"Set organization to {organization}")
    logger.info(f"Set project_id to {project_id}")

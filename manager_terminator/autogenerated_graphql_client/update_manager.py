from uuid import UUID

from .base_model import BaseModel


class UpdateManager(BaseModel):
    manager_update: "UpdateManagerManagerUpdate"


class UpdateManagerManagerUpdate(BaseModel):
    uuid: UUID


UpdateManager.update_forward_refs()
UpdateManagerManagerUpdate.update_forward_refs()

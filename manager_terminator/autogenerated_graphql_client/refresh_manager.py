from typing import Any
from typing import List
from typing import Optional
from uuid import UUID

from .base_model import BaseModel


class RefreshManager(BaseModel):
    manager_refresh: "RefreshManagerManagerRefresh"


class RefreshManagerManagerRefresh(BaseModel):
    objects: List[UUID]
    page_info: "RefreshManagerManagerRefreshPageInfo"


class RefreshManagerManagerRefreshPageInfo(BaseModel):
    next_cursor: Optional[Any]


RefreshManager.update_forward_refs()
RefreshManagerManagerRefresh.update_forward_refs()
RefreshManagerManagerRefreshPageInfo.update_forward_refs()

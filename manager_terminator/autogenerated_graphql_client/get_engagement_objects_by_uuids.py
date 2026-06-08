from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEngagementObjectsByUuids(BaseModel):
    engagements: "GetEngagementObjectsByUuidsEngagements"


class GetEngagementObjectsByUuidsEngagements(BaseModel):
    objects: List["GetEngagementObjectsByUuidsEngagementsObjects"]


class GetEngagementObjectsByUuidsEngagementsObjects(BaseModel):
    validities: List["GetEngagementObjectsByUuidsEngagementsObjectsValidities"]


class GetEngagementObjectsByUuidsEngagementsObjectsValidities(BaseModel):
    uuid: UUID
    person_response: (
        "GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponse"
    )
    validity: "GetEngagementObjectsByUuidsEngagementsObjectsValiditiesValidity"


class GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponse(BaseModel):
    validities: List[
        "GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponseValidities"
    ]


class GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponseValidities(
    BaseModel
):
    uuid: UUID
    validity: "GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponseValiditiesValidity"


class GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponseValiditiesValidity(
    BaseModel
):
    from_: Optional[datetime] = Field(alias="from")
    to: Optional[datetime]


class GetEngagementObjectsByUuidsEngagementsObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEngagementObjectsByUuids.update_forward_refs()
GetEngagementObjectsByUuidsEngagements.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjects.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValidities.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponse.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponseValidities.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPersonResponseValiditiesValidity.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValiditiesValidity.update_forward_refs()

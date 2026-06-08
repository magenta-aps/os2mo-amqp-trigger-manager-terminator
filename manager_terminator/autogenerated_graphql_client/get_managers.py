from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetManagers(BaseModel):
    managers: "GetManagersManagers"


class GetManagersManagers(BaseModel):
    objects: List["GetManagersManagersObjects"]


class GetManagersManagersObjects(BaseModel):
    validities: List["GetManagersManagersObjectsValidities"]


class GetManagersManagersObjectsValidities(BaseModel):
    uuid: UUID
    person_response: Optional["GetManagersManagersObjectsValiditiesPersonResponse"]
    validity: "GetManagersManagersObjectsValiditiesValidity"


class GetManagersManagersObjectsValiditiesPersonResponse(BaseModel):
    validities: List["GetManagersManagersObjectsValiditiesPersonResponseValidities"]


class GetManagersManagersObjectsValiditiesPersonResponseValidities(BaseModel):
    engagements_response: "GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponse"


class GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponse(
    BaseModel
):
    objects: List[
        "GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjects"
    ]


class GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjects(
    BaseModel
):
    validities: List[
        "GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjectsValidities"
    ]


class GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjectsValidities(
    BaseModel
):
    uuid: UUID
    validity: "GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjectsValiditiesValidity"


class GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjectsValiditiesValidity(
    BaseModel
):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetManagersManagersObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetManagers.update_forward_refs()
GetManagersManagers.update_forward_refs()
GetManagersManagersObjects.update_forward_refs()
GetManagersManagersObjectsValidities.update_forward_refs()
GetManagersManagersObjectsValiditiesPersonResponse.update_forward_refs()
GetManagersManagersObjectsValiditiesPersonResponseValidities.update_forward_refs()
GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponse.update_forward_refs()
GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjects.update_forward_refs()
GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjectsValidities.update_forward_refs()
GetManagersManagersObjectsValiditiesPersonResponseValiditiesEngagementsResponseObjectsValiditiesValidity.update_forward_refs()
GetManagersManagersObjectsValiditiesValidity.update_forward_refs()

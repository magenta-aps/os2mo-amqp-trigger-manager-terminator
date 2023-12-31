# Generated by ariadne-codegen on 2023-10-31 10:04
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEngagementObjectsByUuid(BaseModel):
    engagements: "GetEngagementObjectsByUuidEngagements"


class GetEngagementObjectsByUuidEngagements(BaseModel):
    objects: List["GetEngagementObjectsByUuidEngagementsObjects"]


class GetEngagementObjectsByUuidEngagementsObjects(BaseModel):
    objects: List["GetEngagementObjectsByUuidEngagementsObjectsObjects"]


class GetEngagementObjectsByUuidEngagementsObjectsObjects(BaseModel):
    uuid: UUID
    org_unit: List["GetEngagementObjectsByUuidEngagementsObjectsObjectsOrgUnit"]
    person: List["GetEngagementObjectsByUuidEngagementsObjectsObjectsPerson"]
    validity: "GetEngagementObjectsByUuidEngagementsObjectsObjectsValidity"


class GetEngagementObjectsByUuidEngagementsObjectsObjectsOrgUnit(BaseModel):
    uuid: UUID


class GetEngagementObjectsByUuidEngagementsObjectsObjectsPerson(BaseModel):
    uuid: UUID


class GetEngagementObjectsByUuidEngagementsObjectsObjectsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEngagementObjectsByUuid.update_forward_refs()
GetEngagementObjectsByUuidEngagements.update_forward_refs()
GetEngagementObjectsByUuidEngagementsObjects.update_forward_refs()
GetEngagementObjectsByUuidEngagementsObjectsObjects.update_forward_refs()
GetEngagementObjectsByUuidEngagementsObjectsObjectsOrgUnit.update_forward_refs()
GetEngagementObjectsByUuidEngagementsObjectsObjectsPerson.update_forward_refs()
GetEngagementObjectsByUuidEngagementsObjectsObjectsValidity.update_forward_refs()

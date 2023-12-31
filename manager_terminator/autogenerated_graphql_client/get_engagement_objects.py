# Generated by ariadne-codegen on 2023-10-31 13:27
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEngagementObjects(BaseModel):
    engagements: "GetEngagementObjectsEngagements"


class GetEngagementObjectsEngagements(BaseModel):
    objects: List["GetEngagementObjectsEngagementsObjects"]


class GetEngagementObjectsEngagementsObjects(BaseModel):
    objects: List["GetEngagementObjectsEngagementsObjectsObjects"]


class GetEngagementObjectsEngagementsObjectsObjects(BaseModel):
    org_unit: List["GetEngagementObjectsEngagementsObjectsObjectsOrgUnit"]
    validity: "GetEngagementObjectsEngagementsObjectsObjectsValidity"
    person: List["GetEngagementObjectsEngagementsObjectsObjectsPerson"]


class GetEngagementObjectsEngagementsObjectsObjectsOrgUnit(BaseModel):
    uuid: UUID
    name: str


class GetEngagementObjectsEngagementsObjectsObjectsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetEngagementObjectsEngagementsObjectsObjectsPerson(BaseModel):
    uuid: UUID
    engagements: List["GetEngagementObjectsEngagementsObjectsObjectsPersonEngagements"]
    manager_roles: List[
        "GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRoles"
    ]


class GetEngagementObjectsEngagementsObjectsObjectsPersonEngagements(BaseModel):
    uuid: UUID
    org_unit: List[
        "GetEngagementObjectsEngagementsObjectsObjectsPersonEngagementsOrgUnit"
    ]
    validity: "GetEngagementObjectsEngagementsObjectsObjectsPersonEngagementsValidity"


class GetEngagementObjectsEngagementsObjectsObjectsPersonEngagementsOrgUnit(BaseModel):
    uuid: UUID


class GetEngagementObjectsEngagementsObjectsObjectsPersonEngagementsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRoles(BaseModel):
    uuid: UUID
    org_unit: List[
        "GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRolesOrgUnit"
    ]
    validity: "GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRolesValidity"


class GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRolesOrgUnit(BaseModel):
    uuid: UUID


class GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRolesValidity(
    BaseModel
):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEngagementObjects.update_forward_refs()
GetEngagementObjectsEngagements.update_forward_refs()
GetEngagementObjectsEngagementsObjects.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjects.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsOrgUnit.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsValidity.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsPerson.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsPersonEngagements.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsPersonEngagementsOrgUnit.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsPersonEngagementsValidity.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRoles.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRolesOrgUnit.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsPersonManagerRolesValidity.update_forward_refs()

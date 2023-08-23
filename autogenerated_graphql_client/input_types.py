# Generated by ariadne-codegen on 2023-08-23 10:09
# Source: schema.graphql

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class AddressCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    org_unit: Optional[UUID] = None
    person: Optional[UUID] = None
    employee: Optional[UUID] = None
    engagement: Optional[UUID] = None
    visibility: Optional[UUID] = None
    validity: "RAValidityInput"
    user_key: Optional[str] = None
    value: str
    address_type: UUID


class AddressTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class AddressUpdateInput(BaseModel):
    uuid: UUID
    org_unit: Optional[UUID] = None
    person: Optional[UUID] = None
    employee: Optional[UUID] = None
    engagement: Optional[UUID] = None
    visibility: Optional[UUID] = None
    validity: "RAValidityInput"
    user_key: Optional[str] = None
    value: Optional[str] = None
    address_type: Optional[UUID] = None


class AssociationCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    user_key: Optional[str] = None
    primary: Optional[UUID] = None
    validity: "RAValidityInput"
    person: Optional[UUID] = None
    employee: Optional[UUID] = None
    org_unit: UUID
    association_type: UUID


class AssociationTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class AssociationUpdateInput(BaseModel):
    uuid: UUID
    user_key: Optional[str] = None
    primary: Optional[UUID] = None
    validity: "RAValidityInput"
    person: Optional[UUID] = None
    employee: Optional[UUID] = None
    org_unit: Optional[UUID] = None
    association_type: Optional[UUID] = None


class ClassCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    name: str
    user_key: str
    facet_uuid: UUID
    scope: Optional[str] = None
    published: str = "Publiceret"
    parent_uuid: Optional[UUID] = None
    example: Optional[str] = None
    owner: Optional[UUID] = None


class ClassUpdateInput(BaseModel):
    uuid: Optional[UUID] = None
    name: str
    user_key: str
    facet_uuid: UUID
    scope: Optional[str] = None
    published: str = "Publiceret"
    parent_uuid: Optional[UUID] = None
    example: Optional[str] = None
    owner: Optional[UUID] = None


class EmployeeCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    user_key: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    nickname_given_name: Optional[str] = None
    nickname_surname: Optional[str] = None
    seniority: Optional[Any] = None
    cpr_no: Optional[Any] = None
    cpr_number: Optional[str] = None
    given_name: Optional[str] = None
    givenname: Optional[str] = None
    surname: str


class EmployeeTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class EmployeeUpdateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: Optional[datetime] = None
    uuid: UUID
    user_key: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    nickname_given_name: Optional[str] = None
    nickname_surname: Optional[str] = None
    seniority: Optional[Any] = None
    cpr_no: Optional[Any] = None
    cpr_number: Optional[str] = None
    given_name: Optional[str] = None
    givenname: Optional[str] = None
    surname: Optional[str] = None
    validity: Optional["RAValidityInput"] = None


class EngagementCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    user_key: Optional[str] = None
    primary: Optional[UUID] = None
    validity: "RAValidityInput"
    extension_1: Optional[str] = None
    extension_2: Optional[str] = None
    extension_3: Optional[str] = None
    extension_4: Optional[str] = None
    extension_5: Optional[str] = None
    extension_6: Optional[str] = None
    extension_7: Optional[str] = None
    extension_8: Optional[str] = None
    extension_9: Optional[str] = None
    extension_10: Optional[str] = None
    employee: Optional[UUID] = None
    person: Optional[UUID] = None
    org_unit: UUID
    engagement_type: UUID
    job_function: UUID


class EngagementTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class EngagementUpdateInput(BaseModel):
    uuid: UUID
    user_key: Optional[str] = None
    primary: Optional[UUID] = None
    validity: "RAValidityInput"
    extension_1: Optional[str] = None
    extension_2: Optional[str] = None
    extension_3: Optional[str] = None
    extension_4: Optional[str] = None
    extension_5: Optional[str] = None
    extension_6: Optional[str] = None
    extension_7: Optional[str] = None
    extension_8: Optional[str] = None
    extension_9: Optional[str] = None
    extension_10: Optional[str] = None
    employee: Optional[UUID] = None
    person: Optional[UUID] = None
    org_unit: Optional[UUID] = None
    engagement_type: Optional[UUID] = None
    job_function: Optional[UUID] = None


class FacetCreateInput(BaseModel):
    user_key: str
    published: str = "Publiceret"


class FacetUpdateInput(BaseModel):
    user_key: str
    published: str = "Publiceret"
    uuid: UUID


class ITSystemCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    user_key: str
    name: str
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: Optional[datetime] = None


class ITUserCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    primary: Optional[UUID] = None
    person: Optional[UUID] = None
    org_unit: Optional[UUID] = None
    engagement: Optional[UUID] = None
    validity: "RAValidityInput"
    user_key: str
    itsystem: UUID
    type: str = "it"


class ITUserTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class ITUserUpdateInput(BaseModel):
    uuid: UUID
    primary: Optional[UUID] = None
    person: Optional[UUID] = None
    org_unit: Optional[UUID] = None
    engagement: Optional[UUID] = None
    validity: "RAValidityInput"
    user_key: Optional[str] = None
    itsystem: Optional[UUID] = None


class KLECreateInput(BaseModel):
    uuid: Optional[UUID] = None
    user_key: Optional[str] = None
    org_unit: UUID
    kle_aspects: List[UUID]
    kle_number: UUID
    validity: "RAValidityInput"


class KLETerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class KLEUpdateInput(BaseModel):
    uuid: UUID
    user_key: Optional[str] = None
    kle_number: Optional[UUID] = None
    kle_aspects: Optional[List[UUID]] = None
    org_unit: Optional[UUID] = None
    validity: "RAValidityInput"


class LeaveCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    person: UUID
    engagement: UUID
    leave_type: UUID
    validity: "RAValidityInput"


class ManagerCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    user_key: Optional[str] = None
    person: Optional[UUID] = None
    responsibility: List[UUID]
    org_unit: UUID
    manager_level: UUID
    manager_type: UUID
    validity: "RAValidityInput"
    type: str = "manager"


class ManagerTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class ManagerUpdateInput(BaseModel):
    uuid: UUID
    validity: "RAValidityInput"
    user_key: Optional[str] = None
    person: Optional[UUID] = None
    responsibility: Optional[List[UUID]] = None
    org_unit: Optional[UUID] = None
    manager_type: Optional[UUID] = None
    manager_level: Optional[UUID] = None


class OrganisationCreate(BaseModel):
    municipality_code: Optional[int]


class OrganisationUnitCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    name: str
    user_key: Optional[str] = None
    parent: Optional[UUID] = None
    org_unit_type: UUID
    time_planning: Optional[UUID] = None
    org_unit_level: Optional[UUID] = None
    org_unit_hierarchy: Optional[UUID] = None
    validity: "RAValidityInput"


class OrganisationUnitTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class OrganisationUnitUpdateInput(BaseModel):
    uuid: UUID
    validity: "RAValidityInput"
    name: Optional[str] = None
    user_key: Optional[str] = None
    parent: Optional[UUID] = None
    org_unit_type: Optional[UUID] = None
    org_unit_level: Optional[UUID] = None
    org_unit_hierarchy: Optional[UUID] = None
    time_planning: Optional[UUID] = None


class RAValidityInput(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime] = None


class RoleCreateInput(BaseModel):
    uuid: Optional[UUID] = None
    user_key: Optional[str] = None
    org_unit: UUID
    person: UUID
    role_type: UUID
    validity: "RAValidityInput"


class RoleTerminateInput(BaseModel):
    from_: Optional[datetime] = Field(alias="from", default=None)
    to: datetime
    uuid: UUID


class RoleUpdateInput(BaseModel):
    uuid: UUID
    user_key: Optional[str] = None
    org_unit: Optional[UUID] = None
    role_type: Optional[UUID] = None
    validity: "RAValidityInput"


AddressCreateInput.update_forward_refs()
AddressTerminateInput.update_forward_refs()
AddressUpdateInput.update_forward_refs()
AssociationCreateInput.update_forward_refs()
AssociationTerminateInput.update_forward_refs()
AssociationUpdateInput.update_forward_refs()
ClassCreateInput.update_forward_refs()
ClassUpdateInput.update_forward_refs()
EmployeeCreateInput.update_forward_refs()
EmployeeTerminateInput.update_forward_refs()
EmployeeUpdateInput.update_forward_refs()
EngagementCreateInput.update_forward_refs()
EngagementTerminateInput.update_forward_refs()
EngagementUpdateInput.update_forward_refs()
FacetCreateInput.update_forward_refs()
FacetUpdateInput.update_forward_refs()
ITSystemCreateInput.update_forward_refs()
ITUserCreateInput.update_forward_refs()
ITUserTerminateInput.update_forward_refs()
ITUserUpdateInput.update_forward_refs()
KLECreateInput.update_forward_refs()
KLETerminateInput.update_forward_refs()
KLEUpdateInput.update_forward_refs()
LeaveCreateInput.update_forward_refs()
ManagerCreateInput.update_forward_refs()
ManagerTerminateInput.update_forward_refs()
ManagerUpdateInput.update_forward_refs()
OrganisationCreate.update_forward_refs()
OrganisationUnitCreateInput.update_forward_refs()
OrganisationUnitTerminateInput.update_forward_refs()
OrganisationUnitUpdateInput.update_forward_refs()
RAValidityInput.update_forward_refs()
RoleCreateInput.update_forward_refs()
RoleTerminateInput.update_forward_refs()
RoleUpdateInput.update_forward_refs()
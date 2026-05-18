from datetime import datetime
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from ._testing__create_employee import TestingCreateEmployee
from ._testing__create_employee import TestingCreateEmployeeEmployeeCreate
from ._testing__create_engagement import TestingCreateEngagement
from ._testing__create_engagement import TestingCreateEngagementEngagementCreate
from ._testing__create_manager import TestingCreateManager
from ._testing__create_manager import TestingCreateManagerManagerCreate
from ._testing__create_org_unit import TestingCreateOrgUnit
from ._testing__create_org_unit import TestingCreateOrgUnitOrgUnitCreate
from ._testing__terminate_engagement import TestingTerminateEngagement
from ._testing__terminate_engagement import (
    TestingTerminateEngagementEngagementTerminate,
)
from .async_base_client import AsyncBaseClient
from .base_model import UNSET
from .base_model import UnsetType
from .get_engagement_objects import GetEngagementObjects
from .get_engagement_objects import GetEngagementObjectsEngagements
from .get_engagement_objects_by_uuids import GetEngagementObjectsByUuids
from .get_engagement_objects_by_uuids import GetEngagementObjectsByUuidsEngagements
from .get_managers import GetManagers
from .get_managers import GetManagersManagers
from .input_types import EmployeeCreateInput
from .input_types import EngagementCreateInput
from .input_types import ManagerCreateInput
from .input_types import ManagerFilter
from .input_types import OrganisationUnitCreateInput
from .terminate_manager import TerminateManager
from .terminate_manager import TerminateManagerManagerTerminate
from .update_manager import UpdateManager
from .update_manager import UpdateManagerManagerUpdate


def gql(q: str) -> str:
    return q


class GraphQLClient(AsyncBaseClient):
    async def get_managers(self, filter: ManagerFilter) -> GetManagersManagers:
        query = gql("""
            query GetManagers($filter: ManagerFilter!) {
              managers(filter: $filter) {
                objects {
                  validities {
                    uuid
                    org_unit {
                      uuid
                    }
                    person {
                      engagements(filter: {from_date: null, to_date: null}) {
                        uuid
                        org_unit {
                          uuid
                        }
                        validity {
                          from
                          to
                        }
                      }
                    }
                    validity {
                      from
                      to
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"filter": filter}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetManagers.parse_obj(data).managers

    async def terminate_manager(
        self,
        uuid: UUID,
        terminate_to: datetime,
        terminate_from: Union[Optional[datetime], UnsetType] = UNSET,
    ) -> TerminateManagerManagerTerminate:
        query = gql("""
            mutation TerminateManager($uuid: UUID!, $terminate_from: DateTime, $terminate_to: DateTime!) {
              manager_terminate(
                input: {uuid: $uuid, from: $terminate_from, to: $terminate_to}
              ) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {
            "uuid": uuid,
            "terminate_from": terminate_from,
            "terminate_to": terminate_to,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TerminateManager.parse_obj(data).manager_terminate

    async def update_manager(
        self,
        uuid: UUID,
        vacant_from: datetime,
        vacant_to: Union[Optional[datetime], UnsetType] = UNSET,
    ) -> UpdateManagerManagerUpdate:
        query = gql("""
            mutation UpdateManager($uuid: UUID!, $vacant_from: DateTime!, $vacant_to: DateTime) {
              manager_update(
                input: {uuid: $uuid, validity: {from: $vacant_from, to: $vacant_to}, person: null}
              ) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {
            "uuid": uuid,
            "vacant_from": vacant_from,
            "vacant_to": vacant_to,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UpdateManager.parse_obj(data).manager_update

    async def get_engagement_objects(
        self, engagement_uuid: UUID
    ) -> GetEngagementObjectsEngagements:
        query = gql("""
            query GetEngagementObjects($engagement_uuid: UUID!) {
              engagements(filter: {uuids: [$engagement_uuid]}) {
                objects {
                  validities {
                    org_unit {
                      uuid
                    }
                    validity {
                      from
                      to
                    }
                    person {
                      uuid
                      engagements(filter: {from_date: null, to_date: null}) {
                        uuid
                        org_unit {
                          uuid
                        }
                        validity {
                          from
                          to
                        }
                      }
                      manager_roles {
                        uuid
                        org_unit {
                          uuid
                        }
                        validity {
                          from
                          to
                        }
                      }
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"engagement_uuid": engagement_uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEngagementObjects.parse_obj(data).engagements

    async def get_engagement_objects_by_uuids(
        self, engagement_uuids: List[UUID]
    ) -> GetEngagementObjectsByUuidsEngagements:
        query = gql("""
            query GetEngagementObjectsByUuids($engagement_uuids: [UUID!]!) {
              engagements(filter: {uuids: $engagement_uuids, from_date: null, to_date: null}) {
                objects {
                  validities {
                    uuid
                    org_unit {
                      uuid
                    }
                    person {
                      uuid
                    }
                    validity {
                      from
                      to
                    }
                  }
                }
              }
            }
            """)
        variables: dict[str, object] = {"engagement_uuids": engagement_uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEngagementObjectsByUuids.parse_obj(data).engagements

    async def _testing__create_employee(
        self, input: EmployeeCreateInput
    ) -> TestingCreateEmployeeEmployeeCreate:
        query = gql("""
            mutation _Testing_CreateEmployee($input: EmployeeCreateInput!) {
              employee_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateEmployee.parse_obj(data).employee_create

    async def _testing__create_engagement(
        self, input: EngagementCreateInput
    ) -> TestingCreateEngagementEngagementCreate:
        query = gql("""
            mutation _Testing_CreateEngagement($input: EngagementCreateInput!) {
              engagement_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateEngagement.parse_obj(data).engagement_create

    async def _testing__create_manager(
        self, input: ManagerCreateInput
    ) -> TestingCreateManagerManagerCreate:
        query = gql("""
            mutation _Testing_CreateManager($input: ManagerCreateInput!) {
              manager_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateManager.parse_obj(data).manager_create

    async def _testing__create_org_unit(
        self, input: OrganisationUnitCreateInput
    ) -> TestingCreateOrgUnitOrgUnitCreate:
        query = gql("""
            mutation _Testing_CreateOrgUnit($input: OrganisationUnitCreateInput!) {
              org_unit_create(input: $input) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateOrgUnit.parse_obj(data).org_unit_create

    async def _testing__terminate_engagement(
        self, uuid: UUID, to: datetime
    ) -> TestingTerminateEngagementEngagementTerminate:
        query = gql("""
            mutation _Testing_TerminateEngagement($uuid: UUID!, $to: DateTime!) {
              engagement_terminate(input: {uuid: $uuid, to: $to}) {
                uuid
              }
            }
            """)
        variables: dict[str, object] = {"uuid": uuid, "to": to}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingTerminateEngagement.parse_obj(data).engagement_terminate

from uuid import UUID

from .base_model import BaseModel


class TestingTerminateEngagement(BaseModel):
    engagement_terminate: "TestingTerminateEngagementEngagementTerminate"


class TestingTerminateEngagementEngagementTerminate(BaseModel):
    uuid: UUID


TestingTerminateEngagement.update_forward_refs()
TestingTerminateEngagementEngagementTerminate.update_forward_refs()

from uuid import UUID

from app.clients import survey_service_client


async def get_surveys_by_creator_id(creator_id: UUID):
    return await survey_service_client.fetch_surveys_by_creator_id(creator_id)

from pydantic import BaseModel


class CreateIncidentRequest(BaseModel):
    title: str
    description: str
    service: str
    created_by: str
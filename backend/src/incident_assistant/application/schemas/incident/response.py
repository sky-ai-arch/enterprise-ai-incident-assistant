from pydantic import BaseModel, ConfigDict


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    service: str

    severity: str
    status: str

    created_by: str
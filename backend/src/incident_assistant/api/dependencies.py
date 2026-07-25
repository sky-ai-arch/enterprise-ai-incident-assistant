from incident_assistant.domain.repositories.incident_repository import (
    IncidentRepository,
)
from incident_assistant.infrastructure.persistence.memory.incident_repository import (
    InMemoryIncidentRepository,
)

_repository = InMemoryIncidentRepository()


def get_incident_repository() -> IncidentRepository:
    """
    Dependency provider.

    Returns the application's IncidentRepository implementation.
    """

    return _repository
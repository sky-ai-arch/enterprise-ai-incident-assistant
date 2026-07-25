from dataclasses import dataclass
from enum import Enum


class EvidenceType(str, Enum):
    LOG = "log"
    METRIC = "metric"
    DEPLOYMENT = "deployment"
    GITHUB = "github"
    KUBERNETES = "kubernetes"
    DOCUMENT = "document"


@dataclass(slots=True)
class Evidence:
    source: str
    evidence_type: EvidenceType
    content: str
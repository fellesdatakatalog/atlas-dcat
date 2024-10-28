from enum import Enum
from typing import Dict


class ResourceEnum(Enum):
    DATASET = "dataset"
    DATA_SERVICE = "data-service"
    CONCEPT = "concept"
    INFORMATION_MODEL = "information-model"
    SERVICE = "service"
    EVENT = "event"


resource_type_map: Dict[str, ResourceEnum] = {
    "dataset": ResourceEnum.DATASET,
    "data-service": ResourceEnum.DATA_SERVICE,
    "concept": ResourceEnum.CONCEPT,
    "information-model": ResourceEnum.INFORMATION_MODEL,
    "service": ResourceEnum.SERVICE,
    "event": ResourceEnum.EVENT,
}

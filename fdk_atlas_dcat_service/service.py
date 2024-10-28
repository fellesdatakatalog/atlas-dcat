"""Function for doing parse job"""

from typing import Any, Callable, Dict
from fdk_rdf_parser import (
    parse_dataset_as_dict,
    parse_concept_as_dict,
    parse_information_model_as_dict,
    parse_service_as_dict,
    parse_event_as_dict,
    parse_dataservice_as_dict,
)

from fdk_atlas_dcat_service.model import ResourceEnum

ParsedReturnType = Dict[str, Any]

parser_func_map: Dict[
    ResourceEnum,
    Callable[
        [str],
        ParsedReturnType,
    ],
] = {
    ResourceEnum.DATASET: parse_dataset_as_dict,
    ResourceEnum.DATA_SERVICE: parse_dataservice_as_dict,
    ResourceEnum.CONCEPT: parse_concept_as_dict,
    ResourceEnum.INFORMATION_MODEL: parse_information_model_as_dict,
    ResourceEnum.SERVICE: parse_service_as_dict,
    ResourceEnum.EVENT: parse_event_as_dict,
}


def parse_resource(rdf_data: str, resource_type: ResourceEnum) -> ParsedReturnType:
    """Parses RDF data according to the given resource type and returns it as a JSON string"""
    return parser_func_map[resource_type](rdf_data)

"""Helper utilities for parsing query parameters into Beacon request models."""

import json
from typing import Annotated

from fastapi import Query

from beacon_api.models.request import (
    BeaconRequestBody,
    BeaconRequestParameters,
    FilteringTerm,
    RequestedGranularity,
)


def parse_filters_from_string(filters_str: str | None) -> list[FilteringTerm] | None:
    """
    Parse filter string into list of FilteringTerm objects.

    Supports two formats per Beacon v2 specification:
    1. POST/JSON format: JSON string with filter objects
       Example: '[{"id":"HP:0001250"},{"id":"PATO:0000011","operator":">","value":"P70Y"}]'
    2. GET format: Comma-separated filter IDs with optional operators
       Example: 'NCIT:C6975,PATO_0000011:>:P70Y,HP_0032443:%cancer%'

    Args:
        filters_str: Filter string in either JSON or comma-separated format

    Returns:
        List of FilteringTerm objects or None if no filters provided

    Raises:
        ValueError: If filter string is invalid or doesn't match FilteringTerm schema
    """
    if not filters_str:
        return None

    # Try JSON format first (POST requests)
    if filters_str.strip().startswith("[") or filters_str.strip().startswith("{"):
        try:
            filters_data = json.loads(filters_str)

            # Handle single filter object
            if isinstance(filters_data, dict):
                return [FilteringTerm(**filters_data)]

            # Handle array of filter objects
            if isinstance(filters_data, list):
                return [FilteringTerm(**f) for f in filters_data]

            raise ValueError("JSON filters must be an object or array of objects")

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in filters parameter: {e}") from e
        except Exception as e:
            raise ValueError(f"Invalid filter format: {e}") from e

    # Parse comma-separated format (GET requests)
    # Per Beacon v2 spec:
    # - Simple ontology: NCIT:C6975 or HP:0001250
    # - With underscores: PATO_0000011 (gets converted to PATO:0000011)
    # - With operator: PATO_0000011:>P70Y (no colon between operator and value!)
    # - With wildcards: HP_0032443:%cancer%
    try:
        filters = []
        for filter_str in filters_str.split(","):
            filter_str = filter_str.strip()
            if not filter_str:
                continue

            # Check for operator pattern: ID:operatorVALUE or ID_operatorVALUE
            # Operators can be: =, >, <, !, >=, <=
            operator_match = None
            for op in [">=", "<=", "=", ">", "<", "!"]:
                # Try to find operator in the string
                if f":{op}" in filter_str or f"_{op}" in filter_str:
                    # Split on operator
                    if f":{op}" in filter_str:
                        parts = filter_str.split(f":{op}", 1)
                    else:
                        parts = filter_str.split(f"_{op}", 1)

                    if len(parts) == 2:
                        filter_id = parts[0].replace("_", ":")
                        value = parts[1]
                        # Try to convert value to number if possible
                        try:
                            if "." in value and not value.startswith("%"):
                                value = float(value)
                            elif value.isdigit():
                                value = int(value)
                        except ValueError:
                            pass  # Keep as string
                        filters.append(
                            FilteringTerm(id=filter_id, operator=op, value=value)
                        )
                        operator_match = True
                        break

            if not operator_match:
                # Simple ontology filter - just replace underscores with colons
                filter_id = filter_str.replace("_", ":")
                filters.append(FilteringTerm(id=filter_id))

        return filters if filters else None

    except Exception as e:
        raise ValueError(
            f"Invalid filter format. Use comma-separated IDs or JSON: {e}"
        ) from e


def create_request_body_from_params(
    skip: int = 0,
    limit: int = 10,
    granularity: RequestedGranularity = RequestedGranularity.RECORD,
    filters: str | None = None,
) -> BeaconRequestBody:
    """
    Create a BeaconRequestBody from query parameters.

    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        granularity: Requested granularity of response
        filters: JSON string of filters (single object or array)

    Returns:
        BeaconRequestBody with parsed parameters

    Raises:
        ValueError: If filters parameter contains invalid JSON or filter data
    """
    parsed_filters = parse_filters_from_string(filters)

    return BeaconRequestBody(
        meta=BeaconRequestParameters(
            pagination={"skip": skip, "limit": limit},
            requested_granularity=granularity,
        ),
        filters=parsed_filters,
    )


# Type aliases for FastAPI dependency injection
PaginationSkip = Annotated[int, Query(ge=0, description="Number of records to skip")]
PaginationLimit = Annotated[
    int,
    Query(
        ge=1,
        le=100,
        description="Maximum number of records to return",
    ),
]
FilterParam = Annotated[
    str | None,
    Query(
        description='Filters in JSON or comma-separated format. JSON: [{"id":"HP:0001250"}] or comma-separated: NCIT:C6975,PATO_0000011:>:P70Y',
    ),
]
GranularityParam = Annotated[
    RequestedGranularity,
    Query(
        default=RequestedGranularity.BOOLEAN,
        description="Requested granularity of the response (default: boolean)",
    ),
]

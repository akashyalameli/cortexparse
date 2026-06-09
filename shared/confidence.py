from typing import Optional

from shared.template_schema import get_field_confidence
from shared.template_schema import get_schema_fields


def calculate_confidence(
    extracted_data: dict,
    template_schema: Optional[dict] = None
):

    if not extracted_data:
        return 0.0

    fields = extracted_data.get(
        "fields",
        {}
    )

    if not fields and not template_schema:
        return 0.0

    confidence_scores = []

    if template_schema:

        schema_fields = get_schema_fields(
            template_schema
        )

        for field_name in schema_fields:

            confidence_scores.append(
                get_field_confidence(
                    fields.get(field_name)
                )
            )

    else:

        for field_data in fields.values():

            confidence = get_field_confidence(
                field_data
            )

            confidence_scores.append(
                confidence
            )

    if not confidence_scores:
        return 0.0

    average_confidence = (
        sum(confidence_scores)
        / len(confidence_scores)
    )

    return round(
        average_confidence,
        2
    )

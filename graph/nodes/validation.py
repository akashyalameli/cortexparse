from shared.confidence import calculate_confidence
from shared.config.settings import settings
from shared.template_schema import get_field_confidence
from shared.template_schema import get_field_value
from shared.template_schema import get_required_fields
from shared.template_schema import get_schema_fields
from shared.template_schema import normalize_extracted_data_to_schema


def get_missing_required_fields(
    data: dict,
    template_schema: dict
):

    fields = data.get(
        "fields",
        {}
    )

    missing_required_fields = []

    for field_name in get_required_fields(template_schema):

        field_value = get_field_value(
            fields.get(field_name)
        )

        if field_value is None or field_value == "":
            missing_required_fields.append(
                field_name
            )

    return missing_required_fields


def get_low_confidence_fields(
    data: dict,
    template_schema: dict,
    threshold: float
):

    fields = data.get(
        "fields",
        {}
    )

    schema_fields = get_schema_fields(
        template_schema
    )

    low_confidence_fields = []

    for field_name in schema_fields:

        confidence = get_field_confidence(
            fields.get(field_name)
        )

        if confidence < threshold:
            low_confidence_fields.append(
                field_name
            )

    return low_confidence_fields


def get_field_confidence_scores(
    data: dict,
    template_schema: dict
):

    fields = data.get(
        "fields",
        {}
    )

    return {
        field_name: round(
            get_field_confidence(
                fields.get(field_name)
            ),
            2
        )
        for field_name in get_schema_fields(template_schema)
    }


def validation_node(state):

    print("ENTERED NODE: validation_node")

    data = (
        state.get("corrected_data")
        or state.get("extracted_data")
    )

    print("\n=== VALIDATION INPUT ===")
    print(data)
    print("========================\n")

    data = normalize_extracted_data_to_schema(
        data,
        state["template_schema"]
    )

    confidence = calculate_confidence(
        data,
        state["template_schema"]
    )
    missing_required_fields = get_missing_required_fields(
        data,
        state["template_schema"]
    )
    low_confidence_fields = get_low_confidence_fields(
        data,
        state["template_schema"],
        settings.CONFIDENCE_THRESHOLD
    )
    field_confidence_scores = get_field_confidence_scores(
        data,
        state["template_schema"]
    )

    print(f"\nOverall Confidence Score: {confidence}\n")
    print(f"Missing Required Fields: {missing_required_fields}")
    print(f"Low Confidence Fields: {low_confidence_fields}\n")

    return {
        "validated_data": data,
        "overall_confidence_score": confidence,
        "field_confidence_scores": field_confidence_scores,
        "missing_required_fields": missing_required_fields,
        "low_confidence_fields": low_confidence_fields,
        "workflow_status": "DATA_VALIDATED"
    }

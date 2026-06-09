def get_schema_fields(template_schema: dict):

    fields = template_schema.get(
        "fields",
        {}
    )

    if isinstance(fields, dict):

        return fields

    if isinstance(fields, list):

        normalized_fields = {}

        for field in fields:

            if isinstance(field, str):
                normalized_fields[field] = {}

            elif isinstance(field, dict):
                field_name = field.get("name")

                if field_name:
                    normalized_fields[field_name] = field

        return normalized_fields

    return {}


def get_required_fields(template_schema: dict):

    required = template_schema.get(
        "required",
        template_schema.get(
            "required_fields",
            []
        )
    )

    if isinstance(required, str):
        return [required]

    if required:
        return list(required)

    fields = get_schema_fields(
        template_schema
    )

    return [
        field_name
        for field_name, field_schema in fields.items()
        if isinstance(field_schema, dict)
        and field_schema.get("required") is True
    ]


def build_schema_field_contract(template_schema: dict):

    fields = get_schema_fields(
        template_schema
    )

    required_fields = set(
        get_required_fields(template_schema)
    )

    contract = {}

    for field_name, field_schema in fields.items():

        if not isinstance(field_schema, dict):
            field_schema = {}

        contract[field_name] = {
            "required": field_name in required_fields,
            "type": field_schema.get(
                "type",
                "string"
            ),
            "description": field_schema.get(
                "description",
                ""
            )
        }

    return contract


def get_field_value(field_data):

    if isinstance(field_data, dict):
        return field_data.get("value")

    return field_data


def get_field_confidence(field_data):

    if not isinstance(field_data, dict):
        return 0.0

    confidence = field_data.get(
        "confidence"
    )

    if confidence is None:
        return 0.0

    try:
        return float(confidence)

    except (TypeError, ValueError):
        return 0.0


def normalize_extracted_data_to_schema(
    data: dict,
    template_schema: dict
):

    if not isinstance(data, dict):
        data = {}

    normalized_data = {
        "document_type": data.get(
            "document_type"
        ),
        "fields": {}
    }

    fields = data.get(
        "fields",
        {}
    )

    if not isinstance(fields, dict):
        fields = {}

    for field_name in get_schema_fields(template_schema):

        field_data = fields.get(
            field_name
        )

        if isinstance(field_data, dict):

            field_value = field_data.get(
                "value"
            )
            confidence = get_field_confidence(
                field_data
            )

        else:

            field_value = field_data
            confidence = 0.0

        normalized_data["fields"][field_name] = {
            "value": field_value,
            "confidence": round(
                confidence,
                2
            )
        }

    return normalized_data

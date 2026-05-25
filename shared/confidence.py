def calculate_confidence(extracted_data: dict):

    if not extracted_data:
        return 0.0

    fields = extracted_data.get("fields", {})

    if not fields:
        return 0.20

    populated_fields = [
        value
        for value in fields.values()
        if value
    ]

    completeness = (
        len(populated_fields)
        / len(fields)
    )

    confidence = 0.60 + (completeness * 0.35)

    return round(
        min(confidence, 0.98),
        2
    )

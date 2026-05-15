def calculate_confidence(extracted_data: dict):

    if not extracted_data:
        return 0.0

    field_count = len(
        extracted_data.get("fields", {})
    )

    if field_count == 0:
        return 0.25

    return min(0.5 + (field_count * 0.1), 0.95)

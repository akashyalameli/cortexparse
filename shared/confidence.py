def calculate_confidence(extracted_data: dict):

    if not extracted_data:
        return 0.0

    fields = extracted_data.get(
        "fields",
        {}
    )

    if not fields:
        return 0.0

    confidence_scores = []

    for field_data in fields.values():

        if not isinstance(field_data, dict):
            continue

        confidence = field_data.get(
            "confidence"
        )

        if confidence is None:
            continue

        confidence_scores.append(
            float(confidence)
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

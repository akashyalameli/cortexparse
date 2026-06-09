from shared.config.settings import settings


CONFIDENCE_THRESHOLD = settings.CONFIDENCE_THRESHOLD


def has_required_field_failures(state):

    return bool(
        state.get(
            "missing_required_fields",
            []
        )
    )


def extraction_validation_router(state):

    confidence = state["overall_confidence_score"]

    print("\n=== EXTRACTION ROUTER ===")
    print(f"Confidence: {confidence}")
    print(f"Missing required fields: {state.get('missing_required_fields', [])}")
    print("=========================\n")

    if confidence >= CONFIDENCE_THRESHOLD and not has_required_field_failures(state):
        return "publisher"

    return "correction"


def correction_validation_router(state):

    confidence = state["overall_confidence_score"]

    print("\n=== CORRECTION ROUTER ===")
    print(f"Confidence: {confidence}")
    print(f"Missing required fields: {state.get('missing_required_fields', [])}")
    print("=========================\n")

    if confidence >= CONFIDENCE_THRESHOLD and not has_required_field_failures(state):
        return "publisher"

    return "string_refinement"


def refinement_validation_router(state):

    confidence = state["overall_confidence_score"]

    print("\n=== REFINEMENT ROUTER ===")
    print(f"Confidence: {confidence}")
    print(f"Missing required fields: {state.get('missing_required_fields', [])}")
    print("=========================\n")

    if confidence >= CONFIDENCE_THRESHOLD and not has_required_field_failures(state):
        return "publisher"

    return "human_review"

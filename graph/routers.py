CONFIDENCE_THRESHOLD = 0.85


def extraction_validation_router(state):

    confidence = state["overall_confidence_score"]

    print("\n=== EXTRACTION ROUTER ===")
    print(f"Confidence: {confidence}")
    print("=========================\n")

    if confidence >= CONFIDENCE_THRESHOLD:
        return "publisher"

    return "correction"


def correction_validation_router(state):

    confidence = state["overall_confidence_score"]

    print("\n=== CORRECTION ROUTER ===")
    print(f"Confidence: {confidence}")
    print("=========================\n")

    if confidence >= CONFIDENCE_THRESHOLD:
        return "publisher"

    return "string_refinement"


def refinement_validation_router(state):

    confidence = state["overall_confidence_score"]

    print("\n=== REFINEMENT ROUTER ===")
    print(f"Confidence: {confidence}")
    print("=========================\n")

    if confidence >= CONFIDENCE_THRESHOLD:
        return "publisher"

    return "human_review"

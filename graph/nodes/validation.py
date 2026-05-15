from shared.confidence import calculate_confidence


def validation_node(state):

    data = (
        state["corrected_data"]
        if state["corrected_data"]
        else state["extracted_data"]
    )

    confidence = calculate_confidence(data)

    state["overall_confidence_score"] = confidence

    state["workflow_status"] = "DATA_VALIDATED"

    return state

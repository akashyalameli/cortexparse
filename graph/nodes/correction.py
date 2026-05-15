def correction_node(state):

    corrected = state["extracted_data"]

    corrected["correction_attempted"] = True

    current_confidence = state["overall_confidence_score"]

    improved_confidence = min(
        current_confidence + 0.10,
        0.95
    )

    state["corrected_data"] = corrected

    state["overall_confidence_score"] = improved_confidence

    state["workflow_status"] = "DATA_CORRECTED"

    return state

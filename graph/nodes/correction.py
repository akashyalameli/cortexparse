def correction_node(state):

    state["corrected_data"] = state["extracted_data"]

    state["workflow_status"] = "DATA_CORRECTED"

    return state

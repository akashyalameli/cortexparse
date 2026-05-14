def extraction_node(state):

    state["extracted_data"] = {
        "dummy_field": "dummy_value"
    }

    state["workflow_status"] = "DATA_EXTRACTED"

    return state

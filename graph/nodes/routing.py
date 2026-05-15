def routing_node(state):

    document_type = state["document_type"]

    if document_type == "simple":
        model = "qwen2.5:3b"

    else:
        model = "qwen2.5vl:7b"

    state["selected_model"] = model

    state["workflow_status"] = "MODEL_SELECTED"

    return state

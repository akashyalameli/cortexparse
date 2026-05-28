def routing_node(state):

    print("ENTERED NODE: routing_node")

    document_type = state["document_type"]

    if document_type in [
        "simple",
        "receipt"
    ]:
        model = "qwen2.5vl:3b"  # execution_tier = "FAST_LOCAL"
    
    elif document_type in [
        "invoice",
        "form",
        "id_card"
    ]:

        model = "qwen2.5vl:7b"  # execution_tier = "ACCURATE_LOCAL"

    else:
        model = "qwen2.5vl:7b"  # execution_tier = "ESCALATED" | Actually need qwen3:14b but cannot run it with just 32GB RAM. May use remote API in the future if confidence score is low.
    
    print("\n=== SELECTED MODEL ===")
    print(model)
    print("======================\n")

    state["selected_model"] = model  # Don't use model 7b for simple ones, as it's resource intensive and slow.

    state["workflow_status"] = "MODEL_SELECTED"

    return state

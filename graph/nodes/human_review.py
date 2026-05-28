def human_review_node(state):

    print("ENTERED NODE: human_review_node")

    state["requires_human_review"] = True

    state["workflow_status"] = "HUMAN_REVIEW_REQUIRED"

    print("\n=== HUMAN REVIEW REQUIRED ===\n")

    return state

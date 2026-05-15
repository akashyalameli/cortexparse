CONFIDENCE_THRESHOLD = 0.90


def retry_controller_node(state):

    confidence = state["overall_confidence_score"]

    retry_count = state["retry_count"]

    if confidence >= CONFIDENCE_THRESHOLD:

        state["workflow_status"] = "READY_FOR_PUBLISH"

        return state

    if retry_count >= state["max_retries"]:

        state["requires_human_review"] = True
        state["workflow_status"] = "HUMAN_REVIEW_REQUIRED"

        return state

    state["retry_count"] += 1

    state["workflow_status"] = "RETRYING"

    return state


def retry_router(state):

    confidence = state["overall_confidence_score"]

    retry_count = state["retry_count"]

    if confidence >= CONFIDENCE_THRESHOLD:
        return "publisher"

    if retry_count >= state["max_retries"]:
        return "__end__"

    return "correction"

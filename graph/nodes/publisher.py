from shared.rabbitmq import publish_message


def publisher_node(state):

    publish_message({
        "workflow_id": state["workflow_id"],
        "status": "COMPLETED",
        "confidence": state["overall_confidence_score"]
    })

    state["workflow_status"] = "PUBLISHED"

    return state

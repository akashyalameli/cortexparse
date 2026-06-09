from shared.rabbitmq import publish_message


def build_extraction_payload(state):

    extracted_data = (
        state.get("validated_data")
        or state.get("corrected_data")
        or state.get("extracted_data")
    )

    return {
        "workflow_id": state["workflow_id"],
        "document_id": state["document_id"],
        "status": "COMPLETED",
        "document_type": state["document_type"],
        "template_name": state["template_name"],
        "confidence": state["overall_confidence_score"],
        "field_confidence_scores": state.get(
            "field_confidence_scores",
            {}
        ),
        "missing_required_fields": state.get(
            "missing_required_fields",
            []
        ),
        "low_confidence_fields": state.get(
            "low_confidence_fields",
            []
        ),
        "requires_human_review": state.get(
            "requires_human_review",
            False
        ),
        "extracted_data": extracted_data,
    }


def publisher_node(state):

    print("ENTERED NODE: publisher_node")

    payload = build_extraction_payload(
        state
    )

    response_mode = state.get(
        "response_mode",
        "sync"
    )

    if response_mode == "async":

        publish_message(
            payload
        )

        print("\n=== PUBLISHED ASYNC RESULT ===\n")

        return {
            "workflow_status": "PUBLISHED"
        }

    print("\n=== SYNC RESULT READY ===\n")

    return {
        "response_payload": payload,
        "workflow_status": "COMPLETED"
    }

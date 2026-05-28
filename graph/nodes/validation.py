from shared.confidence import calculate_confidence


def validation_node(state):

    print("ENTERED NODE: validation_node")

    data = (
        state.get("corrected_data")
        or state.get("extracted_data")
    )

    print("\n=== VALIDATION INPUT ===")
    print(data)
    print("========================\n")

    confidence = calculate_confidence(data)

    print(f"\nOverall Confidence Score: {confidence}\n")

    return {
        "overall_confidence_score": confidence,
        "workflow_status": "DATA_VALIDATED"
    }

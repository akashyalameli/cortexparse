from pathlib import Path

from shared.document_storage import delete_document


def cleanup_node(state):

    print("ENTERED NODE: cleanup_node")

    path = Path(state["document_path"])

    if path.exists():

        path.unlink()

    delete_document(
        path.name
    )

    telemetry = dict(
        state.get(
            "telemetry",
            {}
        )
    )

    telemetry["cleanup_completed"] = True

    return {
        "telemetry": telemetry
    }

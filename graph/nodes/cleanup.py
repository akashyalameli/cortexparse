from pathlib import Path

from shared.document_storage import delete_document


def cleanup_node(state):

    path = Path(state["document_path"])

    if path.exists():

        path.unlink()

    delete_document(
        path.name
    )

    state["workflow_status"] = "CLEANED_UP"

    return state

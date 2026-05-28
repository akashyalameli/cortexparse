def document_loader_node(state):

    print("ENTERED NODE: document_loader_node")

    return {
        "document_path": state["document_path"],
        "workflow_status": "DOCUMENT_LOADED"
    }

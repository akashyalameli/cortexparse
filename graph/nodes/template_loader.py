def template_loader_node(state):

    print("ENTERED NODE: template_loader_node")

    #state["workflow_status"] = "TEMPLATE_LOADED"

    return {
        "template_data": state.get(
            "template_data"
        )
    }

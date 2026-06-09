from shared.template_storage import load_template_schema


def template_loader_node(state):

    print("ENTERED NODE: template_loader_node")

    template_name = state["template_name"]

    template_schema = load_template_schema(
        template_name
    )

    return {
        "template_schema": template_schema,
        "workflow_status": "TEMPLATE_LOADED"
    }

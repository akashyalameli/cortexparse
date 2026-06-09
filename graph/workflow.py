from langgraph.graph import START
from langgraph.graph import END
from langgraph.graph import StateGraph

from graph.state import WorkflowState

from graph.nodes.document_loader import document_loader_node
from graph.nodes.template_loader import template_loader_node
from graph.nodes.classification import classification_node
from graph.nodes.routing import routing_node
from graph.nodes.extraction import extraction_node
from graph.nodes.validation import validation_node
from graph.nodes.correction import correction_node
from graph.nodes.string_refinement import string_refinement_node
from graph.nodes.publisher import publisher_node
from graph.nodes.cleanup import cleanup_node
from graph.nodes.human_review import human_review_node

from graph.routers import extraction_validation_router
from graph.routers import correction_validation_router
from graph.routers import refinement_validation_router


workflow = StateGraph(WorkflowState)


# Nodes

workflow.add_node("document_loader", document_loader_node)
workflow.add_node("template_loader", template_loader_node)
workflow.add_node("classification", classification_node)
workflow.add_node("routing", routing_node)
workflow.add_node("extraction", extraction_node)
workflow.add_node("validation_after_extraction", validation_node)
workflow.add_node("correction", correction_node)
workflow.add_node("validation_after_correction", validation_node)
workflow.add_node("string_refinement", string_refinement_node)
workflow.add_node("validation_after_refinement", validation_node)
workflow.add_node("publisher", publisher_node)
workflow.add_node("cleanup", cleanup_node)
workflow.add_node("human_review", human_review_node)


# Linear edges

workflow.add_edge(START, "document_loader")

workflow.add_edge("document_loader", "template_loader")

workflow.add_edge("template_loader", "classification")

workflow.add_edge("classification", "routing")

workflow.add_edge("routing", "extraction")

workflow.add_edge("extraction", "validation_after_extraction")

workflow.add_edge("correction", "validation_after_correction")

workflow.add_edge("string_refinement", "validation_after_refinement")

workflow.add_edge("publisher", "cleanup")

workflow.add_edge("cleanup", END)

workflow.add_edge("human_review", END)


# Conditional routing

workflow.add_conditional_edges(
    "validation_after_extraction",
    extraction_validation_router,
    {
        "publisher": "publisher",
        "correction": "correction"
    }
)

workflow.add_conditional_edges(
    "validation_after_correction",
    correction_validation_router,
    {
        "publisher": "publisher",
        "string_refinement": "string_refinement"
    }
)

workflow.add_conditional_edges(
    "validation_after_refinement",
    refinement_validation_router,
    {
        "publisher": "publisher",
        "human_review": "human_review"
    }
)


# Compile

app_workflow = workflow.compile()

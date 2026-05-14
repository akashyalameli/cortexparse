from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import WorkflowState

from graph.nodes.document_loader import document_loader_node
from graph.nodes.template_loader import template_loader_node
from graph.nodes.routing import routing_node
from graph.nodes.extraction import extraction_node
from graph.nodes.validation import validation_node
from graph.nodes.correction import correction_node
from graph.nodes.publisher import publisher_node


workflow = StateGraph(WorkflowState)

workflow.add_node("document_loader", document_loader_node)
workflow.add_node("template_loader", template_loader_node)
workflow.add_node("routing", routing_node)
workflow.add_node("extraction", extraction_node)
workflow.add_node("validation", validation_node)
workflow.add_node("correction", correction_node)
workflow.add_node("publisher", publisher_node)

workflow.set_entry_point("document_loader")

workflow.add_edge("document_loader", "template_loader")
workflow.add_edge("template_loader", "routing")
workflow.add_edge("routing", "extraction")
workflow.add_edge("extraction", "validation")
workflow.add_edge("validation", "correction")
workflow.add_edge("correction", "publisher")
workflow.add_edge("publisher", END)

app_workflow = workflow.compile()

from pathlib import Path

from shared.ollama_client import client
from shared.prompt_loader import load_prompt
from shared.pdf_processor import convert_pdf_to_images
from shared.image_optimizer import optimize_image


def classification_node(state):

    print("ENTERED NODE: classification_node")

    prompt = load_prompt(
        "prompts/classification/document_classifier.txt"
    )

    document_path = state["document_path"]

    suffix = Path(document_path).suffix.lower()

    image_inputs = []

    if suffix == ".pdf":

        image_inputs = convert_pdf_to_images(
            document_path
        )

        state["document_path"] = image_inputs[0]  # Update the document path to point to the first page image for downstream nodes.

    else:

        image_inputs = [document_path]

    image_inputs = [
        optimize_image(path)
        for path in image_inputs
    ]

    response = client.generate(
        model="qwen2.5vl:3b",
        prompt=prompt,
        images=image_inputs
    )

    document_type = (
        response["response"]
        .strip()
        .lower()
    )

    print("\n=== DOCUMENT TYPE ===")
    print(document_type)
    print("=====================\n")

    state["document_type"] = document_type

    state["workflow_status"] = "DOCUMENT_CLASSIFIED"

    return state

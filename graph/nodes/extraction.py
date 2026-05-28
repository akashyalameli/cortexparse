import json

from pathlib import Path

from shared.image_optimizer import optimize_image
from shared.ollama_client import client
from shared.pdf_processor import convert_pdf_to_images
from shared.prompt_loader import load_prompt


def extraction_node(state):

    print("ENTERED NODE: extraction_node")

    prompt = load_prompt(
        "prompts/extraction/document_extraction.txt"
    )

    print(state["document_path"])

    try:

        document_path = state["document_path"]

        image_inputs = [document_path]

        print("\n=== IMAGE INPUTS ===")
        print(image_inputs)
        print("====================\n")
        
        response = client.generate(
            model=state["selected_model"],
            prompt=prompt,
            images=image_inputs
        )

        raw_response = response["response"]

        print("\n=== RAW MODEL RESPONSE ===")
        print(raw_response)
        print("==========================\n")

        try:
            parsed = json.loads(raw_response)

        except Exception:

            parsed = {
                "raw_response": raw_response
            }

        state["extracted_data"] = parsed

        state["workflow_status"] = "DATA_EXTRACTED"

        return state
    
    except Exception as ex:

        print("\n=== EXTRACTION ERROR ===")
        print(str(ex))
        print("========================\n")

        state["extracted_data"] = {}

        state["workflow_status"] = "EXTRACTION_FAILED"

        return state

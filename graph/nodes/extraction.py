import json

from shared.ollama_client import client
from shared.prompt_loader import load_prompt
from shared.template_schema import build_schema_field_contract


def build_extraction_prompt(
    base_prompt: str,
    template_schema: dict
):

    field_contract = build_schema_field_contract(
        template_schema
    )

    return f"""{base_prompt}

Template schema:
{json.dumps(template_schema, indent=2)}

Field contract:
{json.dumps(field_contract, indent=2)}
"""


def extraction_node(state):

    print("ENTERED NODE: extraction_node")

    prompt = load_prompt(
        "prompts/extraction/document_extraction.txt"
    )

    prompt = build_extraction_prompt(
        prompt,
        state["template_schema"]
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

        return {
            "extracted_data": parsed,
            "workflow_status": "DATA_EXTRACTED"
        }
    
    except Exception as ex:

        print("\n=== EXTRACTION ERROR ===")
        print(str(ex))
        print("========================\n")

        return {
            "extracted_data": {},
            "workflow_status": "EXTRACTION_FAILED"
        }

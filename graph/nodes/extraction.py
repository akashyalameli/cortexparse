import json

from shared.ollama_client import client
from shared.prompt_loader import load_prompt


def extraction_node(state):

    prompt = load_prompt(
        "prompts/extraction/document_extraction.txt"
    )

    print(state["document_path"])

    try:

        response = client.generate(
            model=state["selected_model"],
            prompt=prompt,
            images=[state["document_path"]]
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

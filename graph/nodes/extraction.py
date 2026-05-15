import json

from shared.ollama_client import client
from shared.prompt_loader import load_prompt


def extraction_node(state):

    prompt = load_prompt(
        "prompts/extraction/document_extraction.txt"
    )

    response = client.generate(
        model=state["selected_model"],
        prompt=prompt
    )

    raw_response = response["response"]

    try:
        parsed = json.loads(raw_response)

    except Exception:

        parsed = {
            "raw_response": raw_response
        }

    state["extracted_data"] = parsed

    state["workflow_status"] = "DATA_EXTRACTED"

    return state

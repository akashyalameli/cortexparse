import json

from shared.ollama_client import client
from shared.prompt_loader import load_prompt


def correction_node(state):

    print("ENTERED NODE: correction_node")

    prompt = load_prompt(
        "prompts/correction/data_correction.txt"
    )

    extracted_data = (
        state.get("corrected_data")
        or state.get("extracted_data")
    )

    response = client.generate(
        model="qwen2.5:3b",
        prompt=f"""
            {prompt}

            Input JSON:

            {json.dumps(extracted_data)}
        """
    )

    raw_response = response["response"]

    print("\n=== CORRECTION RESPONSE ===")
    print(raw_response)
    print("===========================\n")

    try:

        corrected = json.loads(raw_response)

    except Exception:

        corrected = extracted_data
    
    original_fields = extracted_data.get(
        "fields",
        {}
    )
    
    corrected_fields = corrected.get(
        "fields",
        {}
    )


    for field_name, corrected_field in corrected_fields.items():

        original_field = original_fields.get(
            field_name,
            {}
        )

        original_confidence = original_field.get(
            "confidence",
            0.50
        )

        improved_confidence = min(
            original_confidence + 0.05,
            0.99
        )

        corrected_field["confidence"] = round(
            improved_confidence,
            2
        )

    return {
        "corrected_data": corrected,
        "workflow_status": "DATA_CORRECTED"
    }

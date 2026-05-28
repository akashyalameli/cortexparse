import copy
import re


IMMUTABLE_FIELDS = [
    "name",
    "full_name",
    "first_name",
    "last_name",
    "middle_name",
    "customer_name",
    "vendor_name",
    "pan",
    "aadhaar",
    "aadhar",
    "passport_number",
    "license_number",
    "invoice_number",
    "account_number",
    "ifsc",
    "gstin"
]


NUMERIC_FIELD_HINTS = [
    "date",
    "amount",
    "year",
    "month",
    "number",
    "invoice",
    "total",
    "tax",
    "pin",
    "zip"
]


OCR_NUMERIC_FIXES = {
    "O": "0",
    "o": "0",
    "I": "1",
    "l": "1",
    "S": "5",
    "B": "8"
}


def normalize_whitespace(value: str):

    return re.sub(
        r"\s+",
        " ",
        value
    ).strip()


def normalize_date(value: str):

    value = value.replace(".", "/")
    value = value.replace("-", "/")

    value = re.sub(
        r"(?<=\d)\s+(?=\d)",
        "/",
        value
    )

    return value


def apply_numeric_ocr_fixes(value: str):

    corrected = []

    for character in value:

        corrected.append(
            OCR_NUMERIC_FIXES.get(
                character,
                character
            )
        )

    return "".join(corrected)


def should_skip_field(field_name: str):

    field_name = field_name.lower()

    return field_name in IMMUTABLE_FIELDS


def looks_numeric(field_name: str):

    field_name = field_name.lower()

    return any(
        hint in field_name
        for hint in NUMERIC_FIELD_HINTS
    )


def refine_field(
    field_name: str,
    value: str
):

    original_value = value

    value = normalize_whitespace(value)

    if should_skip_field(field_name):

        return value, False


    if "date" in field_name.lower():

        value = normalize_date(value)


    if looks_numeric(field_name):

        value = apply_numeric_ocr_fixes(value)


    changed = (
        value != original_value
    )

    return value, changed


def update_confidence(
    original_confidence: float,
    changed: bool
):

    if not changed:

        return round(
            original_confidence,
            2
        )

    improved_confidence = min(
        original_confidence + 0.03,
        0.99
    )

    return round(
        improved_confidence,
        2
    )


def string_refinement_node(state):

    source_data = (
        state.get("corrected_data")
        or state.get("extracted_data")
    )

    refined_data = copy.deepcopy(
        source_data
    )

    fields = refined_data.get(
        "fields",
        {}
    )

    refined_fields = {}

    for field_name, field_data in fields.items():

        if not isinstance(field_data, dict):

            refined_fields[field_name] = field_data
            continue


        value = field_data.get(
            "value"
        )

        confidence = field_data.get(
            "confidence",
            0.50
        )


        if not isinstance(value, str):

            refined_fields[field_name] = field_data
            continue


        refined_value, changed = refine_field(
            field_name,
            value
        )


        updated_confidence = update_confidence(
            confidence,
            changed
        )


        refined_fields[field_name] = {
            "value": refined_value,
            "confidence": updated_confidence
        }


    refined_data["fields"] = refined_fields


    print("\n=== STRING REFINEMENT ===")
    print(refined_fields)
    print("=========================\n")


    return {
        "corrected_data": refined_data,
        "workflow_status": "STRING_REFINED"
    }

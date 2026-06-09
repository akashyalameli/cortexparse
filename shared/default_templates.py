templates = {
    "logo.json": {
        "template_name": "logo",
        "document_type": "simple",
        "confidence_threshold": 0.85,
        "fields": {
            "name": {
                "required": True,
                "type": "string"
            },
            "description": {
                "required": False,
                "type": "string"
            }
        }
    },
    "pan.json": {
        "template_name": "pan",
        "document_type": "id_card",
        "confidence_threshold": 0.85,
        "fields": {
            "name": {
                "required": True,
                "type": "string"
            },
            "father_name": {
                "required": False,
                "type": "string"
            },
            "date_of_birth": {
                "required": True,
                "type": "date"
            },
            "pan_number": {
                "required": True,
                "type": "string"
            }
        }
    },
    "aadhaar.json": {
        "template_name": "aadhaar",
        "document_type": "id_card",
        "confidence_threshold": 0.85,
        "fields": {
            "name": {
                "required": True,
                "type": "string"
            },
            "date_of_birth": {
                "required": False,
                "type": "date"
            },
            "gender": {
                "required": False,
                "type": "string"
            },
            "aadhaar_number": {
                "required": True,
                "type": "string"
            }
        }
    },
    "form.json": {
        "template_name": "form",
        "document_type": "structured",
        "confidence_threshold": 0.85,
        "fields": {
            "name": {
                "required": False,
                "type": "string"
            },
            "email": {
                "required": False,
                "type": "string"
            },
            "phone": {
                "required": False,
                "type": "string"
            },
            "address": {
                "required": False,
                "type": "string"
            }
        }
    },
    "prescription.json": {
        "template_name": "prescription",
        "document_type": "handwritten",
        "confidence_threshold": 0.85,
        "fields": {
            "patient_name": {
                "required": True,
                "type": "string"
            },
            "doctor_name": {
                "required": False,
                "type": "string"
            },
            "visit_date": {
                "required": False,
                "type": "date"
            },
            "medications": {
                "required": True,
                "type": "array"
            }
        }
    }
}

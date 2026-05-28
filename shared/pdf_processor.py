from pathlib import Path

import fitz


def convert_pdf_to_images(
    pdf_path: str
):

    pdf_document = fitz.open(pdf_path)

    output_images = []

    zoom = 2.0  # zoom = 5.0 takes 15+ minutes to extract data, with a 32GB RAM and no GPU.

    matrix = fitz.Matrix(
        zoom,
        zoom
    )

    #for page_index in range(len(pdf_document)):  # Only convert the first page for now to save time and resources. Upgrade in the future.
    for page_index in range(min(1, len(pdf_document))):

        page = pdf_document[page_index]

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        image_path = (
            Path("tmp")
            / f"{Path(pdf_path).stem}_page_{page_index + 1}.jpg"
        )

        pix.save(str(image_path))

        output_images.append(
            str(image_path)
        )

    return output_images

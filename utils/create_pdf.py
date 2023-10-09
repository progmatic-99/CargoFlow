from django.template.loader import render_to_string
from django.shortcuts import HttpResponse
from io import BytesIO

import weasyprint
import os
import zipfile
from rms.settings import BASE_DIR


def create_pdf(filename: str, ctx, template: str):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={filename}"

    html_content = render_to_string(template, ctx).encode("utf-8")

    weasyprint.HTML(string=html_content).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(
                f"{BASE_DIR}/shipping/static/shipping/css/sb-admin-2.min.css"
            )
        ],
    )

    return response


def create_zip(voyage, bol_data, template: str):
    filenames = []
    for qs in bol_data:
        bol = qs.first()
        ctx = {"bol": qs, "voyage": voyage}
        path = f"{BASE_DIR}/{bol.bol_number}.pdf"
        filenames.append(path)

        html_content = render_to_string(template, ctx).encode("utf-8")
        weasyprint.HTML(string=html_content).write_pdf(
            target=path,
            stylesheets=[
                weasyprint.CSS(
                    f"{BASE_DIR}/shipping/static/shipping/css/sb-admin-2.min.css"
                )
            ],
        )

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in filenames:
            zipf.write(file, os.path.basename(file))

    zip_filename = f"{voyage}-bols.zip"
    # Construct the response to send the ZIP file for download
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={zip_filename}"
    return response

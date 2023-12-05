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

    weasyprint.HTML(string=html_content).write_pdf(response)

    return response


def create_zip(voyage, bol_data, zip_filename, template: str):
    filenames = []
    for qs in bol_data:
        bol = qs.first()
        ctx = {"bol": qs, "voyage": voyage}
        path = f"{BASE_DIR}/{bol.bol_number}.pdf"
        filenames.append(path)

        html_content = render_to_string(template, ctx).encode("utf-8")
        weasyprint.HTML(string=html_content).write_pdf(target=path)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in filenames:
            zipf.write(file, os.path.basename(file))

    # Construct the response to send the ZIP file for download
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={zip_filename}"
    return response


def create_do_zip(voyage, bol_data, zip_filename, template: str):
    filenames = []
    for bols in bol_data:
        consignee = bols[0].consignee
        ctx = {"bols": bols, "voyage": voyage, "consignee": consignee}
        path = f"{BASE_DIR}/{consignee}-Delivery-Order.pdf"
        filenames.append(path)

        html_content = render_to_string(template, ctx).encode("utf-8")
        weasyprint.HTML(string=html_content).write_pdf(target=path)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in filenames:
            zipf.write(file, os.path.basename(file))

    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={zip_filename}"
    return response

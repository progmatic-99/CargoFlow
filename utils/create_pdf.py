from django.template.loader import render_to_string
from django.shortcuts import HttpResponse

import weasyprint
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

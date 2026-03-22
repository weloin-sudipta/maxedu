import frappe
import base64
import os
from typing import Optional


# ─────────────────────────────────────────────────────────
#  🔧 Internal helper: render a template with data
# ─────────────────────────────────────────────────────────
def _render_template(template_name: str, data: dict) -> str:
    """Load an HTML template from pdf-service/templates/ and replace {{vars}}."""
    # frappe.get_app_path("maxedu") → .../apps/maxedu/maxedu  (the Python pkg dir)
    # We go one level up to .../apps/maxedu, then into pdf-service/templates/
    # NOTE: we do NOT pass "pdf-service" through frappe.get_app_path because
    #       Frappe normalises path segments and converts hyphens to underscores.
    app_pkg_dir = frappe.get_app_path("maxedu")           # .../apps/maxedu/maxedu
    app_root    = os.path.dirname(app_pkg_dir)            # .../apps/maxedu
    template_path = os.path.join(
        app_root, "pdf-service", "templates", template_name
    )

    if not os.path.exists(template_path):
        frappe.throw(
            f"PDF template '{template_name}' not found.<br>"
            f"Expected path: <code>{template_path}</code>"
        )

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Handle {{#if var}}...{{/if}} conditional blocks
    import re
    def replace_if_block(match):
        var_name = match.group(1).strip()
        inner    = match.group(2)
        value    = data.get(var_name, "")
        return inner if value else ""

    html = re.sub(
        r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}',
        replace_if_block,
        html,
        flags=re.DOTALL
    )

    # Also strip any stray {{else}} sections that remain
    html = re.sub(r'\{\{else\}\}.*?\{\{/if\}\}', '', html, flags=re.DOTALL)

    # Simple {{key}} substitution
    for key, value in data.items():
        html = html.replace("{{" + key + "}}", str(value) if value is not None else "")

    return html


# ─────────────────────────────────────────────────────────
#  🔧 Internal helper: call PDF service and save to Frappe
# ─────────────────────────────────────────────────────────
def _generate_and_save(html: str, filename: str, options: Optional[dict] = None) -> str:
    """Generate PDF using Frappe's native get_pdf, save result as a Frappe File, return URL."""
    from frappe.utils.pdf import get_pdf

    try:
        # Generate raw PDF bytes using Frappe's native wkhtmltopdf wrapper
        pdf_bytes = get_pdf(html, options=options)
    except Exception as e:
        frappe.throw(f"PDF generation failed: {str(e)}")

    # Frappe File requires base64-encoded content + decode=True for binary files.
    # Passing raw bytes with decode=False results in a corrupt / "Page not found" file.
    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "content": pdf_b64,
        "is_private": 0,
        "decode": True          # Frappe will base64-decode and write to disk
    })
    file_doc.save(ignore_permissions=True)
    frappe.db.commit()

    return file_doc.file_url


# ─────────────────────────────────────────────────────────────────────────────
#  📄 PUBLIC API — Admit Card PDF
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def generate_admit_card_pdf(exam_type=None):
    """
    Generate a beautifully designed Admit Card PDF for the current student.

    Returns:
        { "file_url": "/files/admit_card_<student>_<exam_type>.pdf" }
    """
    from maxedu.api_folder.exam import get_admit_data

    # 1. Fetch admit data
    admit = get_admit_data(exam_type=exam_type)

    # student is a Frappe Document object — convert to plain dict
    student_doc = admit.get("student")
    if hasattr(student_doc, "as_dict"):
        student = student_doc.as_dict()
    else:
        student = dict(student_doc) if student_doc else {}

    exams = admit.get("exams", [])

    if not exams:
        frappe.throw("No exams found to generate admit card.")

    # 2. Build exam rows HTML
    exam_rows_html = ""
    for idx, exam in enumerate(exams, start=1):
        exam_rows_html += f"""
        <tr>
          <td>{idx}</td>
          <td class="subject-cell">{exam.get('subject', '')}</td>
          <td class="date-cell">{exam.get('date', '')}</td>
          <td class="time-cell">{_fmt_time(exam.get('start_time'))} – {_fmt_time(exam.get('end_time'))}</td>
          <td><span class="room-chip">{exam.get('room') or '—'}</span></td>
          <td>{exam.get('max_score', '')}</td>
        </tr>
        """

    # Derive date range from exams list
    exam_dates = [e.get("date") for e in exams if e.get("date")]
    exam_start = min(exam_dates) if exam_dates else ""
    exam_end = max(exam_dates) if exam_dates else ""

    first_exam = exams[0]

    # 3. Template data
    institution_name = "MaxEdu Institution"

    template_data = {
        "institution_name"  : institution_name or "MaxEdu Institution",
        "exam_type"         : exam_type or "All Subjects",
        "exam_start_date"   : _fmt_date(exam_start),
        "exam_end_date"     : _fmt_date(exam_end),
        "generated_on"      : frappe.utils.formatdate(frappe.utils.nowdate(), "dd MMM yyyy"),
        "student_name"      : student.get("student_name") or student.get("name"),
        "student_id"        : student.get("name"),
        "student_email"     : student.get("student_email_id") or frappe.session.user,
        "student_image"     : student.get("image") or "",
        "program"           : first_exam.get("program") or "—",
        "academic_year"     : first_exam.get("academic_year") or "—",
        "student_group"     : first_exam.get("student_group") or "—",
        "exam_rows"         : exam_rows_html,
    }

    # 4. Render template
    html = _render_template("admit_card.html", template_data)

    # 5. Generate PDF filename
    safe_exam = (exam_type or "all").replace(" ", "_").lower()
    safe_student = student.get("name", "student").replace(" ", "_").replace("-", "_")
    filename = f"admit_card_{safe_student}_{safe_exam}.pdf"

    # 6. Call PDF service & save
    file_url = _generate_and_save(html, filename, options={"format": "A4"})

    return {"file_url": file_url, "student_name": student.get("student_name"), "exam_type": exam_type}


# ─────────────────────────────────────────────────────────────────────────────
#  📄 PUBLIC API — Generic PDF from raw HTML
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def generate_pdf_from_html(html, filename="document.pdf", options=None):
    """
    Universal endpoint: pass any HTML, get a stored PDF URL back.
    Useful for notices, certificates, reports — anything.

    Body:
        html     : full HTML string
        filename : output file name
        options  : { format, landscape, margin }
    """
    if not html:
        frappe.throw("html is required")

    import json
    if isinstance(options, str):
        try:
            options = json.loads(options)
        except Exception:
            options = {}

    file_url = _generate_and_save(html, filename, options or {})
    return {"file_url": file_url}


# ─────────────────────────────────────────────────────────────────────────────
#  📄 PUBLIC API — Template-based PDF
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def generate_pdf_from_template(template_name, data, filename="document.pdf", options=None):
    """
    Render an HTML template (in pdf-service/templates/) with data dict, then
    convert to PDF and return stored URL.

    Examples:
        template_name: "admit_card.html" | "certificate.html" | "notice.html"
        data: JSON string (Frappe coerces params to string)
    """
    import json

    if isinstance(data, str):
        data = json.loads(data)
    if isinstance(options, str):
        try:
            options = json.loads(options)
        except Exception:
            options = {}

    html = _render_template(template_name, data)
    file_url = _generate_and_save(html, filename, options or {})
    return {"file_url": file_url}


# ─────────────────────────────────────────────────────────────────────────────
#  🔧 Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _fmt_time(t):
    if not t:
        return "—"
    parts = str(t).split(":")
    h = int(parts[0])
    m = parts[1] if len(parts) > 1 else "00"
    suffix = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{m} {suffix}"


def _fmt_date(d):
    if not d:
        return "—"
    try:
        return frappe.utils.formatdate(str(d), "dd MMM yyyy")
    except Exception:
        return str(d)

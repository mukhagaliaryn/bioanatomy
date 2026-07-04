import io
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from core.models import UserSubject
from core.utils.decorators import role_required
import os


def _register_fonts():
    dejavu_dir = '/usr/share/fonts/truetype/dejavu'
    try:
        pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(dejavu_dir, 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(dejavu_dir, 'DejaVuSans-Bold.ttf')))
        return 'DejaVu', 'DejaVu-Bold'
    except Exception:
        return 'Helvetica', 'Helvetica-Bold'


@login_required
@role_required('student')
def certificate_pdf_view(request, subject_id):
    user = request.user
    user_subject = get_object_or_404(UserSubject, user=user, pk=subject_id)

    if not user_subject.is_completed:
        raise Http404

    subject = user_subject.subject
    student_name = f'{user.first_name} {user.last_name}'.strip() or user.email
    author = subject.author or 'Bioanatomy'
    completed_date = user_subject.completed_at
    date_str = completed_date.strftime('%d.%m.%Y') if completed_date else ''
    rating = user_subject.rating

    font_regular, font_bold = _register_fonts()

    buf = io.BytesIO()
    W, H = landscape(A4)
    c = canvas.Canvas(buf, pagesize=landscape(A4))

    # ── Background ──────────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#fff7ed'))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Outer border ────────────────────────────────────────────────────────
    border_pad = 12 * mm
    c.setStrokeColor(colors.HexColor('#f97316'))
    c.setLineWidth(2)
    c.roundRect(border_pad, border_pad, W - 2 * border_pad, H - 2 * border_pad, 10, fill=0, stroke=1)

    # inner thin border
    inner_pad = 16 * mm
    c.setStrokeColor(colors.HexColor('#fed7aa'))
    c.setLineWidth(0.8)
    c.roundRect(inner_pad, inner_pad, W - 2 * inner_pad, H - 2 * inner_pad, 8, fill=0, stroke=1)

    # ── Decorative top stripe ────────────────────────────────────────────────
    stripe_h = 6 * mm
    c.setFillColor(colors.HexColor('#f97316'))
    c.roundRect(border_pad, H - border_pad - stripe_h, W - 2 * border_pad, stripe_h, 6, fill=1, stroke=0)

    # ── "СЕРТИФИКАТ" title ──────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#9a3412'))
    c.setFont(font_bold, 11)
    c.drawCentredString(W / 2, H - 38 * mm, 'СЕРТИФИКАТ')

    # divider line
    c.setStrokeColor(colors.HexColor('#fed7aa'))
    c.setLineWidth(0.6)
    c.line(60 * mm, H - 42 * mm, W - 60 * mm, H - 42 * mm)

    # ── "Берілді" label ─────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#78350f'))
    c.setFont(font_regular, 9)
    c.drawCentredString(W / 2, H - 52 * mm, 'Осы сертификат')

    # ── Student name ────────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#1c1917'))
    c.setFont(font_bold, 28)
    c.drawCentredString(W / 2, H - 70 * mm, student_name)

    # underline
    name_w = c.stringWidth(student_name, font_bold, 28)
    ux = (W - name_w) / 2
    c.setStrokeColor(colors.HexColor('#f97316'))
    c.setLineWidth(1.5)
    c.line(ux, H - 73 * mm, ux + name_w, H - 73 * mm)

    # ── Body text ───────────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#78350f'))
    c.setFont(font_regular, 11)
    c.drawCentredString(W / 2, H - 85 * mm, 'пәнді сәтті аяқтағаны үшін берілді:')

    # ── Subject name ─────────────────────────────────────────────────────────
    c.setFillColor(colors.HexColor('#ea580c'))
    c.setFont(font_bold, 20)
    c.drawCentredString(W / 2, H - 100 * mm, subject.name)

    # ── Rating badge ─────────────────────────────────────────────────────────
    badge_w, badge_h = 36 * mm, 12 * mm
    bx = (W - badge_w) / 2
    by = H - 118 * mm
    c.setFillColor(colors.HexColor('#f97316'))
    c.roundRect(bx, by, badge_w, badge_h, 6, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(font_bold, 11)
    c.drawCentredString(W / 2, by + 3.5 * mm, f'Бағасы: {rating}/100')

    # ── Bottom row: author | date ────────────────────────────────────────────
    bottom_y = inner_pad + 14 * mm

    # Author
    c.setFillColor(colors.HexColor('#78350f'))
    c.setFont(font_regular, 9)
    c.drawString(inner_pad + 10 * mm, bottom_y + 5 * mm, 'Автор / Оқытушы')
    c.setFont(font_bold, 11)
    c.setFillColor(colors.HexColor('#1c1917'))
    c.drawString(inner_pad + 10 * mm, bottom_y - 1 * mm, author)
    # signature line
    c.setStrokeColor(colors.HexColor('#d6d3d1'))
    c.setLineWidth(0.5)
    c.line(inner_pad + 10 * mm, bottom_y - 3 * mm, inner_pad + 70 * mm, bottom_y - 3 * mm)

    # Logo / Platform name (center)
    c.setFillColor(colors.HexColor('#f97316'))
    c.setFont(font_bold, 13)
    c.drawCentredString(W / 2, bottom_y + 3 * mm, 'Bioanatomy')
    c.setFillColor(colors.HexColor('#78350f'))
    c.setFont(font_regular, 8)
    c.drawCentredString(W / 2, bottom_y - 4 * mm, 'bioanatomy.kz')

    # Date
    if date_str:
        c.setFillColor(colors.HexColor('#78350f'))
        c.setFont(font_regular, 9)
        c.drawRightString(W - inner_pad - 10 * mm, bottom_y + 5 * mm, 'Аяқталған күні')
        c.setFont(font_bold, 11)
        c.setFillColor(colors.HexColor('#1c1917'))
        c.drawRightString(W - inner_pad - 10 * mm, bottom_y - 1 * mm, date_str)
        c.setStrokeColor(colors.HexColor('#d6d3d1'))
        c.setLineWidth(0.5)
        c.line(W - inner_pad - 70 * mm, bottom_y - 3 * mm, W - inner_pad - 10 * mm, bottom_y - 3 * mm)

    c.showPage()
    c.save()

    buf.seek(0)
    filename = f'certificate_{user.id}_{subject.id}.pdf'
    response = HttpResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

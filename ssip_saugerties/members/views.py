from io import BytesIO

from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Spacer
from reportlab.platypus import Frame
from reportlab.platypus import Paragraph
from reportlab.platypus import PageTemplate
from reportlab.platypus import BaseDocTemplate

from .models import Member


# Create your views here.
def member_list(request):
    member_list = Member.objects.all()
    return render(request, 'members/member_list.html', {
        'member_list': member_list,
    })


def build_frames(pwidth, pheight, ncols):
    frames = []
    for i in range(ncols):
        f = Frame(x1=(i*((pwidth-30) / ncols)+15),
                  y1=0,
                  width=((pwidth-30) / ncols),
                  height=pheight+2,
                  leftPadding=15,
                  rightPadding=15,
                  topPadding=15,
                  bottomPadding=15,
                  showBoundary=True)
        frames.append(f)
    frames[0].showBoundary=False
    frames[3].showBoundary=False
    return frames


def member_list_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="memberlist.pdf"'

    buffer = BytesIO()

    NCOLUMNS = 4
    PAGE_WIDTH, PAGE_HEIGHT = landscape(letter)

    styles = getSampleStyleSheet()

    ptemplate = PageTemplate(frames=build_frames(PAGE_WIDTH, PAGE_HEIGHT, NCOLUMNS))
    doc = BaseDocTemplate(
        filename=buffer,
        pagesize=landscape(letter),
        pageTemplates=[ptemplate],
        showBoundary=0,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        allowSplitting=0,
        title='SSIP Members',
        author='SSIP',
        _pageBreakQuick=1,
        encrypt=None)

    template = Template("""
<font size="14"><strong>{{ member.last_name }}, {{ member.first_name }}</strong></font>
<br/>

{% if member.address or member.town %}
    {{ member.address }}<br/>
    {% if member.town %} {{ member.town }} NY {% if member.zipcode %} {{ member.zipcode }} {% endif %}<br/>{% endif %}
{% endif %}

{% if member.homephone %}
(Home) {{ member.homephone }}
<br/>
{% endif %}

{% if member.cellphone %}
(Cell) {{ member.cellphone }}
<br/>
{% endif %}

{% if member.email %}
Email: {{ member.email }}
<br/>
{% endif %}

{% if member.birthday %}
<strong>Birthday Month:</strong> {{ member.birthday }}
<br/>
{% endif %}

{% if member.occupation %}
<strong>Occupation</strong>: {{ member.occupation }}
<br/>
{% endif %}

{% if member.hobbies %}
<strong>My Hobbies</strong>: {{ member.hobbies }}
<br/>
{% endif %}

{% if member.canhelp %}
<strong>I can help with</strong>: {{ member.canhelp }}
<br/>
{% endif %}

{% if member.needhelp %}
<strong>I could use help with</strong>: {{ member.needhelp }}
<br/>
{% endif %}

{% if member.comments %}
<strong>Comments</strong>: {{ member.comments }}
{% endif %}
""")

    content = []
    for member in Member.objects.all():
        context = Context({"member": member})
        p = Paragraph(template.render(context), styles["Normal"])
        content.append(p)
        content.append(Spacer(1, 0.2*inch))

    doc.build(content)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

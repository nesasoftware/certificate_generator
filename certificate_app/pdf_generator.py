# pdf_generator.py
from django.http import HttpResponse
from certificate_app.models import Student
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.flowables import Image
import textwrap
from django.shortcuts import reverse

my_Style = ParagraphStyle(
    'My Para style',
    fontName='Times-Roman',
    backColor='#F1F1F1',
    fontSize=16,
    borderColor='#FFFF00',
    borderWidth=2,
    borderPadding=(20, 20, 20),
    leading=20,
    alignment=0
)

hyperlink_Style = ParagraphStyle(
    'Hyperlink style',
    parent=my_Style,
    textColor='blue',
    underline=True,
)

def generate_pdf(response, student_instance):
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; filename="generate.pdf"'

    # Create the PDF object
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create a list to hold the story (elements to be added to the PDF)
    story = []

    # Add image to the PDF
    image_path = 'pictures/Graduation_Certificate.jpg'
    story.append(Image(image_path, width=580, height=400))

    # Add student ID text
    story.append(Paragraph(f"SRC/2024/{student_instance.id}", my_Style))

    # Add student name
    name = student_instance.name
    name_style = ParagraphStyle(
        'Name style',
        parent=my_Style,
        fontSize=32,
        alignment=1  # Center alignment
    )
    story.append(Paragraph(name, name_style))

    # Add the first paragraph with HTML markup
    html_paragraph = '''<b>About this online classes </b><br/>
                        Welcome to our online classes.<br/>
                        You can learn Python, PHP, databases like MySQL, SQLite, and many more.
                        <font face="times" color="blue">We are creating PDF by using ReportLab</font>
                        <i>This is part of our Final report.</i>'''
    story.append(Paragraph(html_paragraph, my_Style))

    # Add the second paragraph with wrapped text
    paragraph = f"Student of {student_instance.college_name}, has successfully completed the academic internship " \
                f"program at SinroRobotics Pvt Ltd in {student_instance.course} under the guidance of {student_instance.mentor_name}. " \
                f"The internship spanned from {student_instance.start_date} to {student_instance.end_date}."
    
    max_line_width = 70  # Maximum characters per line
    lines = textwrap.wrap(paragraph, width=max_line_width)

    wrapped_paragraph_style = ParagraphStyle(
        'Wrapped paragraph style',
        parent=my_Style,
        fontSize=12,
        alignment=1  # Center alignment
    )

    for line in lines:
        story.append(Paragraph(line, wrapped_paragraph_style))

    # Add the date
    story.append(Paragraph(str(student_instance.end_date), my_Style))

    # Add a clickable area to navigate to another HTML page 
    link_text = f"Click here for verification"
    certificate_verification_url = reverse('certificate_verify', args=[student_instance.id])
    hyperlink = '<a href="{}">{}</a>'.format(certificate_verification_url, link_text)
    story.append(Paragraph(hyperlink, hyperlink_Style))

    # Build the PDF
    doc.build(story)
    return response

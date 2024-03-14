from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from certificate_app.models import Student
from .forms import MyForm
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
import os
from django.contrib.auth.models import User
from .models import Student
from django.template import loader
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import pyqrcode 
import io
import png 
from pyqrcode import QRCode
import textwrap
#from .pdf_generator import generate_pdf



# student form page for submitting details
def my_view(request):
    form = MyForm()

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            student_instance = form.save(commit=False)  # Save the form data but don't commit to the database yet
            name = form.cleaned_data['name']
            course = form.cleaned_data['course']
            end_date = form.cleaned_data['end_date']
            student_instance.name = name
            student_instance.course = course
            student_instance.end_date = end_date
            student_instance.save()  # Now, save the modified instance
            
            return redirect('certificate_show', student_id=student_instance.id)  # Redirect to the certificate page

    return render(request, 'student_form.html', {'form': form})


# show the certificate
def certificate_show(request, student_id):
    student_instance = Student.objects.get(id=student_id)
    context = {'student_instance': student_instance}
    return render(request, 'show_certificate.html', context)


# display verification page
def certificate_verification(request, student_id):     
    student_instance = Student.objects.get(id=student_id)
    context = {'student_instance': student_instance}
    return render(request, 'certificate_verification.html', context)


def render_pdf_view(request, student_id):
    # Get the specific Student object based on student_id
    student_instance = get_object_or_404(Student, id=student_id)

    # Create a BytesIO buffer to store the PDF content
    buffer = io.BytesIO()

    # Create the response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="generate.pdf"'

    custom_page_size = (600, 440)
    c = canvas.Canvas(buffer, bottomup=1, pagesize=custom_page_size)
    c.translate(inch, inch)

    desired_width = 596
    desired_height = 436

    
    c.drawImage('pictures\GraduationCertificate.jpg', -0.97*inch, -0.97*inch, width=desired_width, height=desired_height, mask=None)
    font_path = 'static/fonts/Quattrocento-Regular.ttf'
    pdfmetrics.registerFont(TTFont('Quattrocento', font_path))
    c.setFont('Quattrocento', 12)  
    c.drawString(4.5 * inch, 4.5 * inch, f"SRC/2024/{student_instance.id}")
    
    # Register Dancing Script font
    font_path = 'static/fonts/MonteCarlo-Regular.ttf'
    pdfmetrics.registerFont(TTFont('MonteCarlo', font_path))

    # Example name
    name = student_instance.name

    # Set the font for the name
    c.setFont('MonteCarlo', 40)
    c.setFillColor(HexColor('#3c3a3f'))
    # c.setFillColorRGB(0,0,0)
    # Calculate the width of the name in points
    name_width = c.stringWidth(name)

    

    if len(name) < 12:
        left_align_x = 2.4 * inch
        left_align_y = 2.20 * inch
        c.drawString(left_align_x, left_align_y, name)
    elif len(name)<22:
        left_align_x = 1.7 * inch
        left_align_y = 2.20 * inch
        c.drawString(left_align_x, left_align_y, name)
    else:
        center_align_x = (desired_width - name_width) / 2
        center_align_y = 2.20 * inch
        c.drawCentredString(center_align_x, center_align_y, name)

    font_path = 'static/fonts/Quattrocento-Regular.ttf'
    pdfmetrics.registerFont(TTFont('Quattrocento', font_path))
    my_Style = ParagraphStyle(
        'My Para style',
        fontName='Quattrocento',
        fontSize=12,
        leading=20,  # Line height
        charSpace=5.0,  # Character spacing
        alignment='center',
        HexColor='#3c3a3f',
    )
    
    # Define your custom style
    my_Style = getSampleStyleSheet()['BodyText']
    p1 = Paragraph(f'''Student of <b>{student_instance.college_name}</b>, has successfully completed the academic internship
        program at SinroRobotics Pvt Ltd in <b>{student_instance.course}</b> under the guidance of <b>{student_instance.mentor_name}</b>. 
        The internship spanned from <b>{student_instance.start_date}</b> to <b>{student_instance.end_date}</b>.''', my_Style)
    
    width = 940
    height = 400
    p1.wrapOn(c, 450, 50)
    p1.drawOn(c, width-930, height-295)

    c.drawImage('pictures\paragraph-end-line.png', 2.45*inch, 0.7*inch, width=100, height=50,mask=None)

    c.setFont('Quattrocento', 12)
    c.setFillColorRGB(0,0,0)
    c.drawString(4.7*inch, 0.4*inch, str(student_instance.end_date))

    # Generate QR code
    base_url = request.build_absolute_uri('/')
    qr_data = f"{base_url}certificate_verify/{student_instance.id}/"
    qr = pyqrcode.create(qr_data)

    # Save the QR code as BytesIO
    qr_buffer = io.BytesIO()
    qr.png(qr_buffer, scale=6)

    # Save the QR code as a file on the server
    qr_filename = f"qr_code_{student_instance.id}.png"
    qr_path = os.path.join(settings.MEDIA_ROOT, qr_filename)
    qr.png(qr_path, scale=6)

    # Pass the URL or path of the QR code image to the context
    context = {'qr_code_path': qr_path}

    x = 200
    y = -10
    width=50
    height=50
    # Draw the QR code image on the PDF
    qr_image = ImageReader(qr_buffer)
    c.drawImage(qr_image, x, y, width, height)

    

    
    c.showPage()
    c.save()

    # Rewind the buffer to the beginning
    buffer.seek(0)

    # Write the buffer content to the response
    response.write(buffer.read())

    # Close the buffers
    buffer.close()
    qr_buffer.close()

    return response



def pdf_view(request, student_id):
    # Get the student_instance based on student_id
    student_instance = get_object_or_404(Student, id=student_id)

    # # Generate QR code data
    # qr_data = f"student_id={student_instance.id}"

    # Render the template with the PDF content
    template = get_template('generate.html')
    
    # Pass both request and qr_data when calling render_pdf_view
    context = {'pdf_content': render_pdf_view(request, student_instance).content}
    rendered_template = template.render(context)

    # Return the rendered template
    return HttpResponse(rendered_template)


def registration(request):

    return render(request,'registration.html')


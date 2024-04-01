import io
import os
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from django.utils.text import slugify
from .models import Student
from django.conf import settings
from datetime import datetime
from pyqrcode import QRCode
import pyqrcode



def generate_certificate(student_id):
    
    student_instance = Student.objects.get(id=student_id)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Get the specific Student object based on student_id
    student_instance = get_object_or_404(Student, id=student_id)

    # Create a BytesIO buffer to store the PDF content
    buffer = io.BytesIO()

    file_name=f"{student_instance.id}_{slugify(student_instance.name)}_certificate"

    # # Create the response object and it shows pdf page in other tab without downloading
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{file_name}.pdf"'

    # Create the response object and it directly download pdf page 
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'


    #pdf page format
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

    
    # center_align_x = (desired_width - name_width) / 2
    # center_align_y = 2.20 * inch
    # c.drawCentredString(center_align_x, center_align_y, name)

    # Calculate the center coordinates of the canvas
    center_x = desired_width / 2

    # Calculate the starting x-coordinate to center the text
    if len(name) < 10:
        start_x = 2.9 * inch
    else:
        # For longer names, we'll need to adjust the starting x-coordinate to ensure proper center alignment
        start_x = center_x - (name_width / 2)
        
    align_y = 2.20 * inch    
    c.drawCentredString(start_x, align_y, name)
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
    # c.drawString(4.7*inch, 0.4*inch, str(student_instance.end_date))
    c.drawString(4.7*inch, 0.4*inch, str(datetime.now().strftime("%Y-%m-%d")))


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
    print("QR Code Path:", qr_path)
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


    return buffer
 

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from certificate_app.models import Student
from .forms import MyForm, UploadFileForm
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
import csv
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
from django.contrib.auth.decorators import login_required
from datetime import datetime
import zipfile
from io import BytesIO




# student form page for submitting details
@login_required(login_url='login/')
def my_view(request):
    form = MyForm()
    upload_form = UploadFileForm()

    if request.method == 'POST':
        if 'submit_form' in request.POST:
            form = MyForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('upload_success')  # Redirect to the upload success URL
        elif 'upload_csv' in request.POST:
            upload_form = UploadFileForm(request.POST, request.FILES)
            if upload_form.is_valid():
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    # Parse and format dates
                    start_date = datetime.strptime(row['start_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
                    end_date = datetime.strptime(row['end_date'], '%d-%m-%Y').strftime('%Y-%m-%d')

                    Student.objects.create(
                        name=row.get('name', ''),
                        college_name=row.get('college_name', ''),
                        course=row.get('course', ''),
                        start_date=start_date,
                        end_date=end_date,
                        mentor_name=row.get('mentor_name', '')
                    )
                return redirect('upload_success')  # Redirect to the upload success URL

    return render(request, 'student_form.html', {'form': form, 'upload_form': upload_form})

def upload_success(request):
    return render(request, 'upload_success.html')


# display all students
def display_students(request):
    students = Student.objects.all()
    return render(request, 'display_students.html', {'students': students})


# show the certificate
@login_required(login_url='login/')
def certificate_show(request, student_id):
    student_instance = Student.objects.get(id=student_id)
    qr_code_path = f"qr_code_{student_instance.id}.png"
    context = {'student_instance': student_instance, 'qr_code_path': qr_code_path}
    return render(request, 'show_certificate.html', context)



# display verification page
def certificate_verification(request, student_id):     
    student_instance = Student.objects.get(id=student_id)
    context = {'student_instance': student_instance}
    return render(request, 'certificate_verification.html', context)


@login_required(login_url='login/')
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

    # Write the buffer content to the response
    response.write(buffer.read())

    # Close the buffers
    buffer.close()
    qr_buffer.close()

    return response


@login_required(login_url='login/')
def download_students_csv(request):
    # Retrieve all student data
    students = Student.objects.all()

    # Create a BytesIO buffer to store the zip file
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, False) as zip_file:
        for student in students:
        # Create a CSV file for each student
            csv_buffer = io.BytesIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow([b'Name', b'College Name', b'Course', b'Start Date', b'End Date', b'Mentor Name'])  # Ensure bytes-like objects
            csv_writer.writerow([
                student.name.encode('utf-8'),            # Encode strings as bytes
                student.college_name.encode('utf-8'),
                student.course.encode('utf-8'),
                student.start_date.strftime('%Y-%m-%d').encode('utf-8'),  # Format date as string and encode as bytes
                student.end_date.strftime('%Y-%m-%d').encode('utf-8'),    # Format date as string and encode as bytes
                student.mentor_name.encode('utf-8')                        # Encode string as bytes
        ])
        # Create a filename with student ID (adjust as needed)
            filename = f"student_{student.id}.csv"

            # Write the CSV data to the ZipFile
            zip_file.writestr(filename, csv_buffer.getvalue())

    # Set the content type and response headers
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=students.zip'

    return response


@login_required(login_url='login/')
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



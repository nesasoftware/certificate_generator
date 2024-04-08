from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from certificate_app.models import Student, CertificateTypes,Course, Authority, StudentRelatedAuthority
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch
from django.db import IntegrityError
from .forms import MyForm, UploadFileForm
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
import csv
import os
# import tempfile
# from django.http import FileResponse
from django.utils.text import slugify
from django.template import loader
# from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
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
from django.utils import timezone
from django.contrib import messages
import zipfile
from io import BytesIO
from django.core.files.temp import NamedTemporaryFile
from reportlab.lib import colors
from certificate_app.pdf_utils import generate_certificate


# student form page for submitting details
@login_required(login_url='login')
def my_view(request):
    certificate_types = CertificateTypes.objects.all()
    authorities = Authority.objects.all()
    upload_form = UploadFileForm()

    if request.method == 'POST':
        if 'submit_form' in request.POST:
            name = request.POST.get('name')
            college_name = request.POST.get('college_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            mentor_name = request.POST.get('mentor_name')
            issued_date = timezone.now().date()
            certificate_type_id = request.POST.get('certificate_type')
            authority_ids = request.POST.getlist('authority')
            course_id = request.POST.get('courses')
            print("id:",course_id)
            # Fetch the CertificateTypes instance based on the provided certificate_type_id
            certificate_type = CertificateTypes.objects.get(id=certificate_type_id)
            print("certificate_type:",certificate_type)
            # Fetch the Course instance based on the provided course_id
            course = Course.objects.get(id=course_id)
            print("course:",course)

            #Assign the selected course to the student through the CertificateTypes instance
            certificate_type.courses.add(course) 
            print("Added course:", course)

            student = Student.objects.create(
                name=name,
                college_name=college_name,
                start_date=start_date,
                end_date=end_date,
                mentor_name=mentor_name,
                issued_date=issued_date,
                certificate_type_id=certificate_type_id,
                course=course
            )

            # Add selected authorities to the student
            for authority_id in authority_ids:
                authority = Authority.objects.get(id=authority_id)
                StudentRelatedAuthority.objects.create(std=student, authority=authority)

            return redirect('display_students')  # Redirect to the display students page
        

        elif 'upload_csv' in request.POST:
            upload_form = UploadFileForm(request.POST, request.FILES)
            if upload_form.is_valid():
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    start_date = timezone.datetime.strptime(row['start_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
                    end_date = timezone.datetime.strptime(row['end_date'], '%d-%m-%Y').strftime('%Y-%m-%d')

                    authorities = row.get('auth_id', '').split(',')

                    for auth_id in authorities:
                        try:
                            # Get Authority instance based on the custom ID (auth_id)
                            authority = Authority.objects.get(auth_id=auth_id)
                        except Authority.DoesNotExist:
                             # Handle the case where the Authority instance with the provided auth_id doesn't exist
                            print(f"Authority with auth_id {auth_id} does not exist. Skipping this auth_id.")
                            continue
                        
                        # Fetch or create the Course instance based on the provided course_name
                        course_name = row.get('course_name')
                        course = Course.objects.get_or_create(course_name=course_name)

                        # Fetch certificate_type_id from row data
                        certificate_type_id = row.get('certificate_type_id')
                        print("certificate_type_id:", certificate_type_id)

                        try:
                            # Get CertificateTypes instance based on the custom ID
                            certificate_type = CertificateTypes.objects.get(certify_type_id=certificate_type_id)
                        except CertificateTypes.DoesNotExist:
                            # Handle the case where the CertificateTypes instance with the provided certificate_type_id doesn't exist
                            print(f"CertificateTypes with certificate_type_id {certificate_type_id} does not exist. Skipping this row.")
                            continue


                        # Create Student instance for the current row
                        student = Student.objects.create(
                            name=row.get('name', ''),
                            college_name=row.get('college_name', ''),
                            start_date=start_date,
                            end_date=end_date,
                            mentor_name=row.get('mentor_name', ''),
                            issued_date=timezone.now().date(),
                            certificate_type=certificate_type,  
                            course=course
                        # course=row.get('course_name','')
                        )

                        # Create StudentRelatedAuthority instance linking student with authority
                        StudentRelatedAuthority.objects.create(std=student, authority=authority)

                        # Print a message indicating successful processing
                        print("CSV file processed successfully")                       

                return redirect('display_students')
            else:
                # Print form errors if any
                print("Form errors:", upload_form.errors)
        else:
            # Print if 'upload_csv' is not in request.POST
            print("Upload CSV not found in request")

    return render(request, 'student_form.html', {'certificate_types': certificate_types, 'authorities': authorities, 'upload_form': upload_form})

    
def get_courses(request):
    certificate_type_id = request.GET.get('certificate_type_id')
    certificate_type = CertificateTypes.objects.get(id=certificate_type_id)
    courses = certificate_type.courses.all()
    
    return render(request,'student_form.html',{'courses': courses})


    
# display all students
@login_required(login_url='login')
def display_students(request):
    students = Student.objects.all().order_by('-created_at')
    certificate_types = CertificateTypes.objects.all()
    
    # First, you need to retrieve an instance of CertificateTypes
    certificate_type_instance = CertificateTypes.objects.get(pk=2)  # Assuming you're getting the instance by primary key
    
    # Now you can access the courses related to this instance
    courses = certificate_type_instance.courses.all()
    print(courses)

    # You can iterate over the courses or access individual attributes
    # for course in courses:
    #     print(course.course_name)

    return render(request, 'table.html', {'students': students, 'certificate_types': certificate_types,'courses':courses})


# def display_students(request):
#     students = Student.objects.all().order_by('-created_at')  # Order by created_at descending
#     courses = Course.objects.all()  # Fetch all courses initially
#     certificate_types = CertificateTypes.objects.all()
#     certificate_type_id = request.GET.get('certificate_type_id')
#     print(certificate_type_id)
    
#     selected_course_name = request.GET.get('course_name')
    
#     if selected_course_name:
#         # Filter students based on the selected course name
#         students = Student.objects.filter(course__course_name=selected_course_name).order_by('-created_at')
#     else:
#         students = Student.objects.all().order_by('-created_at')
#     return render(request, 'table.html', {'students': students, 'courses': courses, 'certificate_types': certificate_types})



# show the certificate
@login_required(login_url='login')
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



@login_required(login_url='login')
def render_pdf_view(request, student_id):

    # Get the specific Student object based on student_id
    student_instance = get_object_or_404(Student, id=student_id)

    # Get the certificate type associated with the student
    certificate_type_id = student_instance.certificate_type_id
    certificate_type = get_object_or_404(CertificateTypes, id=certificate_type_id)

    # Get the courses related to the certificate type
    courses = certificate_type.courses.first()

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

    
    c.drawImage('pictures\Certificate of Participation Blank.jpg', -0.97*inch, -0.97*inch, width=desired_width, height=desired_height, mask=None)
    font_path = 'static/fonts/Cascadia.ttf'
    pdfmetrics.registerFont(TTFont('Cascadia', font_path))
    c.setFont('Cascadia', 12)  
    current_year = datetime.now().strftime("%Y")
    c.drawString(5.1* inch, 4.75 * inch, f"SRC{current_year}{student_instance.id}")
    
    # Register Dancing Script font
    font_path = 'static/fonts/MTCORSVA.TTF'
    pdfmetrics.registerFont(TTFont('MonteCarlo', font_path))

    
    
    # Example name
    name = student_instance.name

    # Set the font for the name
    # c.setFont('MonteCarlo', font_size)
    # c.setFillColor(HexColor('#c46608'))

    # Define font size thresholds and corresponding font sizes
    font_size_threshold = 30
    default_font_size = 40
    reduced_font_size = 30
    
    # Calculate the width of the name string
    name_width = c.stringWidth(name)
    
    # Calculate the center of the page
    center_x = letter[0] / 2
    
    # Calculate the starting x-coordinate to center the text
    if len(name) < font_size_threshold:
        start_x = 3.2 * inch
        font_size = default_font_size
    else:
        # For longer names, reduce the font size and adjust the starting x-coordinate
        start_x = 3.2 * inch
        # start_x = center_x - (name_width / 2)
        font_size = reduced_font_size
    
    align_y = 1.9 * inch
    
    # Set the font size
    c.setFont('MonteCarlo', font_size)
    c.setFillColor(HexColor('#c46608'))
        
    align_y = 1.9 * inch    
    c.drawCentredString(start_x, align_y, name)
    

    
    font_path = 'static/fonts/Minion-It.ttf'
    pdfmetrics.registerFont(TTFont('Minion Pro', font_path))
    c.setFont('Minion Pro', 12)

    # Define your custom style
    my_Style = getSampleStyleSheet()['BodyText']
    
    my_Style.alignment = 1 
    p1 = Paragraph(f'''<i>Student of <b>{student_instance.college_name}</b>, has successfully completed the academic internship
        program at <b>SinroRobotics Pvt Ltd</b> on <b>{courses}</b> from <b>{student_instance.start_date}</b> to <b>{student_instance.end_date}</b>.</i>''', my_Style)
    
    width = 940
    height = 500
    p1.wrapOn(c, 450, 50)
    p1.drawOn(c, width-930, height-405)

    # Get the StudentRelatedAuthority instance for the given student_id
    student_related_authority = get_object_or_404(StudentRelatedAuthority, std_id=student_id)

    # Accessing the related Student ID
    student_id = student_related_authority.std.id
    print("Related Student ID:", student_id)

    # Accessing the related Authority instance
    authority = student_related_authority.authority

    if authority:
        # Accessing the signature attribute of the related Authority instance
        signature_image_url = str(authority.signature)
        print("Signature Image URL:", signature_image_url)

        c.drawImage('media/' + signature_image_url, 4.4 * inch, 0 * inch, width=80, height=40, mask=None)

    
    #c.drawImage('pictures/Nebu-John-SIgn.png',4.4*inch, 0.1*inch, width=100, height=50,mask=None)

    font_path = 'static/fonts/Quattrocento-Bold.ttf'
    pdfmetrics.registerFont(TTFont('Quattrocento-Bold', font_path))
    c.setFont('Quattrocento-Bold', 12)
    c.setFillColorRGB(0,0,0)
    c.drawString( 0.8*inch, 0.08*inch, str(datetime.now().strftime("%Y-%m-%d")))


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

    x = 6.4* inch
    y = 4.3 * inch
    # x = 200
    # y = -10
    width=50
    height=50
    # Draw the QR code image on the PDF
    qr_image = ImageReader(qr_buffer)
    # c.drawImage(qr_image, x, y, width, height)

    
    c.showPage()
    c.save()

    # Rewind the buffer to the beginning
    buffer.seek(0)

    # Write the buffer content to the response
    response.write(buffer.getvalue())

    # Close the buffers
    buffer.close()
    qr_buffer.close()

    return response



@login_required(login_url='login')
def pdf_view(request, student_id):
    # Generate PDF content for the specific student
    pdf_content = render_pdf_view(request, student_id).content

    # Pass the PDF content to the template context
    context = {'pdf_content': pdf_content}

    # Render the template containing the PDF content
    rendered_template = get_template('generate.html').render(context)

    # Return the rendered template as an HttpResponse
    return HttpResponse(rendered_template)



@login_required(login_url='login')
def download_selected_certificates(request):
    if request.method == 'POST':
        selected_student_ids = request.POST.getlist('selected_students')

        # Create a BytesIO buffer to store the ZIP file content
        zip_buffer = BytesIO()

        # Create a ZIP file to store the certificates
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            for student_id in selected_student_ids:
                # Generate PDF certificate for each selected student
                pdf_content = render_pdf_view(request, student_id).content

                # Retrieve the student object based on the student_id
                student_instance = get_object_or_404(Student, id=student_id)
                student_name = student_instance.name

                # Generate PDF certificate for the selected student
                pdf_content = render_pdf_view(request, student_id).content
                file_name = f"{student_id}_{student_name.replace(' ', '_')}_certificate.pdf"

                # file_name = f"{student_id}_certificate.pdf"

                # Add the PDF content to the ZIP file
                zip_file.writestr(file_name, pdf_content)

        # Rewind the buffer to the beginning
        zip_buffer.seek(0)

        # Create a response to serve the ZIP file
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="certificates.zip"'
        return response

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@login_required(login_url='login')
def index(request):
    total_students = Student.objects.count()
    username = request.user.username  # Accessing the username of the logged-in user
    email=request.user.email
    return render(request, 'index.html',{'total_students':total_students,'username':username,'email':email})



@login_required(login_url='login')
def courses(request):
    username = request.user.username  # Accessing the username of the logged-in user
    email=request.user.email
    context = {
        'username': username,
        'email': email,
         # Pass the URL to the template
    }
    return render(request, 'courses.html',context)


# dashboard search
@login_required(login_url='login')
def search_students(request):
    if request.method == 'POST':
        search_query = request.POST.get('search', '').strip()  # Strip whitespace
        # Filter students based on the search query (case-insensitive)
        # For date fields, we need to handle them differently
        try:
            # Attempt to parse the search query as a date
            search_date = datetime.strptime(search_query, '%Y-%m-%d').date()
            students = Student.objects.filter(
                Q(college_name__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(course__icontains=search_query) |
                Q(mentor_name__icontains=search_query) |
                Q(start_date=search_date) |
                Q(end_date=search_date)
            )
        except ValueError:
            # If the search query is not a valid date, perform regular text search
            students = Student.objects.filter(
                Q(college_name__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(course__icontains=search_query) |
                Q(mentor_name__icontains=search_query)
            )
        return render(request, 'search_results.html', {'students': students})
    return render(request, 'search_results.html')



@login_required(login_url='login')
def edit(request, pk):
    instance_to_be_edited = Student.objects.get(pk=pk)
    
    if request.method == 'POST':
        frm = MyForm(request.POST, instance=instance_to_be_edited)
        if frm.is_valid():
            frm.save()
            return redirect('display_students')  # Redirect after successful form submission
    else:
        frm = MyForm(instance=instance_to_be_edited)
    
    return render(request, 'edit.html', {'form': frm})



@login_required(login_url='login')
def delete(request, pk):
    try:
        student_instance = Student.objects.get(pk=pk)
        student_instance.delete()
        messages.success(request, 'Student record deleted successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'Student record does not exist.')
    
    return redirect('display_students')
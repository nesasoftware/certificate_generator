from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student
from .forms import MyForm
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from .process import html_to_pdf 
from .models import Student
from django.template import loader
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter,A4
from django.conf import settings
import os
from reportlab.pdfbase.ttfonts import TTFont



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


#pdf generation 
def render_pdf_view( c, student_id):
    
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="generate.pdf"'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="generate.pdf"'

    custom_page_size = (620, 440)
    # Create the PDF object, using the response object as its "file."
    c = canvas.Canvas(response, bottomup=1,pagesize=custom_page_size)
    c.translate(inch,inch) #starting point of coordinates

    desired_width = 580
    desired_height = 400

    # Get all objects from the MyModel model
    mymodels = Student.objects.all()

    # Get the specific Student object based on student_id
    student_instance = get_object_or_404(Student, id=student_id)


    for mymodel in mymodels:
        c.drawImage('pictures\Graduation_Certificate.jpg', -0.7*inch, -0.69*inch, width=desired_width, height=desired_height,mask=None)
        c.drawString(4.7*inch, 9.1*inch, f"SRC/2024/{student_instance.id}")

        c.setFont('Helvetica', 32)

        # Example name
        name = mymodel.name

        # Calculate the width of the name in points
        name_width = c.stringWidth(name, 'Helvetica', 12)
        
        center_align_x = (desired_width - name_width) / 2
        center_align_y = 2.20 * inch
         
        # Center-aligned text
        c.drawCentredString(center_align_x, center_align_y, name)


        text_object = c.beginText(0.2 * inch, 5.8 * inch)
        text_object.setFont("Helvetica", 12)
        line1 = text_object.textLine(f"Student of {mymodel.college_name}, has successfully completed the academic internship")
        line2 = text_object.textLine(f"program at SinroRobotics Pvt Ltd in {mymodel.course} under the guidance of {mymodel.mentor_name}.")
        line3 = text_object.textLine(f"The internship spanned from {mymodel.start_date} to {mymodel.end_date}.")

        
        c.drawText(text_object)
            
        c.drawString(4.9*inch, 4.0*inch, str(mymodel.end_date))
       
        c.drawString(2.5*inch, 1.0*inch, "verification link")

    # Close the canvas object    
    c.showPage()
    c.save()

    return response


def pdf_view(request, student_id):
    # Render the template with the PDF content
    template = get_template('generate.html')
    context = {'pdf_content': render_pdf_view(request, canvas.Canvas( bottomup=1, pagesize=letter), student_id).content}
    rendered_template = template.render(context)

    # Return the rendered template
    return HttpResponse(rendered_template) 


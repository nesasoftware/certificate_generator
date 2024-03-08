from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from .forms import MyForm
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.conf import settings
from django.urls import reverse
from django.templatetags.static import static, StaticNode

# student form page submitting details
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



def link_callback(uri, rel):
    # Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    # Use Django's static() function to get the absolute URL
    s_url = StaticNode.handle_simple("static", f"'{uri}'")
    return s_url

#display the pdf page
def render_pdf_view(request, student_id):  
    latest_student = Student.objects.latest('id')
    
    template_path = 'ex.html'
    template = get_template(template_path)
    context = {'student_instance': latest_student}

    # Build the full URL for the background image
    image_url = request.build_absolute_uri(static('images/Graduation_Certificate(3).png'))
    context['background_image_url'] = image_url

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="downloaded_pdf.pdf"'

    pdf_options = {
        'page-size': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': 'utf-8',  
    }

    pisa_status = pisa.CreatePDF(
        html, dest=response, encoding='utf-8', link_callback=link_callback
    )
 


    if pisa_status.err:
        return HttpResponse('Error during PDF generation.', content_type='text/plain')

    return response

def certificate_verification(request,std_id):
    return render(request,'certificate_verification.html')
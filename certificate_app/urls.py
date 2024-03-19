 
from django.urls import path
from .  import views


urlpatterns = [
    
    path('data-submission/', views.my_view, name='student_form'),
    # path('upload-success/', views.upload_success, name='upload_success'),
    path('display-student/', views.display_students, name='display_students'),
    path('render-pdf/<int:student_id>/', views.render_pdf_view, name='render_pdf'),
    path('pdf_view/<int:student_id>/', views.pdf_view, name='pdf_view'),
    path('download_selected_certificates/', views.download_selected_certificates, name='download_selected_certificates'),
    # path('certificate/download-students-certificate/<int:student_id>/', views.download_certificate, name='download_certificate'),
    # path('certificate_show/<int:student_id>/', views.certificate_show, name='certificate_show'),
    path('certification_verification/<int:student_id>/', views.certificate_verification, name='certificate_verify'),
    

]



 
from django.urls import path
from .  import views


urlpatterns = [
    
    path('data-submission/', views.my_view, name='student_form'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('display-student/', views.display_students, name='display_students'),
    path('download-students-csv/', views.download_students_csv, name='download_students_csv'),
    path('certificate_show/<int:student_id>/', views.certificate_show, name='certificate_show'),
    path('render-pdf/<int:student_id>/', views.render_pdf_view, name='render_pdf'),
    path('pdf_view/<int:student_id>/', views.pdf_view, name='pdf_view'),
    path('certification_verification/<int:student_id>/', views.certificate_verification, name='certificate_verify'),
    

]



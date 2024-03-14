 
from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.my_view, name='student_form'),
    path('certificate_show/<int:student_id>/', views.certificate_show, name='certificate_show'),
    path('render-pdf/<int:student_id>/', views.render_pdf_view, name='render_pdf'),
    path('pdf_view/<int:student_id>/', views.pdf_view, name='pdf_view'),
    path('certification_verification/<int:student_id>/', views.certificate_verification, name='certificate_verify'),
    path('register/',views.registration),
]



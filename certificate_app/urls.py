 
from django.urls import path
from .  import views


urlpatterns = [
    path('index/',views.index, name='index'),
    path('courses/',views.courses, name='courses'),
    path('data-submission/', views.my_view, name='student_form'),
    path('display-student/', views.display_students, name='display_students'),
    path('edit/<pk>',views.edit,name='edit'),
    path('delete/<pk>', views.delete, name='delete'),
    path('search/', views.search_students, name='search_students'),
    # path('display-student/search_popup.html', views.search_popup_view, name='search_popup'),
    path('render-pdf/<int:student_id>/', views.render_pdf_view, name='render_pdf'),
    path('render-pdf-workshop/<int:student_id>/', views.render_pdf_workshop, name='render_pdf_workshop'),
    path('render-pdf-summercamp/<int:student_id>/', views.render_pdf_summercamp, name='render_pdf_summercamp'),
    path('pdf_view/<int:student_id>/', views.pdf_view, name='pdf_view'),
    path('download_selected_certificates/', views.download_selected_certificates, name='download_selected_certificates'),
    path('certification_verification/<int:student_id>/', views.certificate_verification, name='certificate_verify'),
]



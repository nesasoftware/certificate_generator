 
from django.urls import path
from .  import views
# from .views import StudentViewSet


urlpatterns = [
    path('index/',views.index, name='index'),
    path('courses/',views.courses, name='courses'),
    path('data-submission/', views.my_view, name='student_form'),
    path('iv-data-submission/', views.student_iv_submit, name='student_iv_form'),
    path('tronix-data-submission/', views.student_tronix_submit, name='student_tronix_form'),
    path('certificates-data/',views.certificates_data, name='certificates_data'),
    path('display-student/', views.display_students, name='display_students'),
    path('display-iv-student/', views.display_iv_students, name='display_iv_students'),
    path('display-tronix-student/', views.display_tronix_students, name='display_tronix_students'),
    path('edit/<pk>',views.edit,name='edit'),
    path('edit-iv/<pk>',views.edit_iv,name='edit_iv'),
    path('edit-tronix/<pk>',views.edit_tronix,name='edit_tronix_details'),
    path('delete/<pk>', views.delete, name='delete'),
    path('delete-iv/<pk>', views.delete_iv, name='delete_iv'),
    path('delete-tronix/<pk>', views.delete_tronix, name='delete_tronix'),
    path('search/', views.search_students, name='search_students'),
    # path('display-student/search_popup.html', views.search_popup_view, name='search_popup'),
    path('render-pdf/<int:student_id>/', views.render_pdf_view, name='render_pdf'),
    path('render-pdf-workshop/<int:student_id>/', views.render_pdf_workshop, name='render_pdf_workshop'),
    path('render-pdf-summercamp/<int:student_id>/', views.render_pdf_summercamp, name='render_pdf_summercamp'),
    path('render-pdf-industrialvisit/<int:student_id>/', views.render_pdf_industrialvisit, name='render_pdf_industrialvisit'),
    path('render-pdf-tronix/<int:student_id>/', views.render_pdf_tronix, name='render_pdf_tronix'),
    path('pdf_view/<int:student_id>/', views.pdf_view, name='pdf_view'),
    path('download_selected_certificates/', views.download_selected_certificates, name='download_selected_certificates'),
    path('download_selected_ivcertificates/', views.download_selected_ivcertificates, name='download_selected_ivcertificates'),
    path('download_selected_tronixcertificates/', views.download_selected_tronixcertificates, name='download_selected_tronixcertificates'),
    #path('certification_verification/<int:student_id>/', views.certificate_verification, name='certificate_verify'),
    
]
from django.urls import path
from . import views

urlpatterns=[
  path('register/',views.registration, name='register'),
  path('',views.login_user, name='login'),
  path('logout/', views.logout_view, name='logout'),
]


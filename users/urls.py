from django.urls import path
from . import views

urlpatterns=[
  path('',views.registration, name='register'),
  path('login/',views.login_user, name='login'),
  path('logout/', views.logout_view, name='logout'),
]


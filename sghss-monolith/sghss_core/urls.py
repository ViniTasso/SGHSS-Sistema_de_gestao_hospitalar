from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/login/', views.login_view, name='login'),
    path('api/patients/register/', views.register_patient_view, name='register-patient'),
]
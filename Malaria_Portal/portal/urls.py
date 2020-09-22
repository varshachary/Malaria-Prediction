from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from portal import views

app_name='portals'

urlpatterns = [
    path('', login_required(views.TemplateView.as_view(template_name = 'portal/home.html')), name='home'),
    path('patient/add/', views.PatientAdd.as_view(), name='patient_add'),
    path('patients/', views.PatientList.as_view(), name='patient_list'),
    path('patients/<int:pk>', views.PatientDetail.as_view(), name='patient_detail'),
    path('patient/diagnosis/', views.Diagnosis.as_view(), name='diagnosis'),
    path('patient/adherence/report/<int:pk>', views.AdherenceTest.as_view(), name='adherence'),
    path('training_data/', views.TrainingData.as_view(), name="training_data"),
]

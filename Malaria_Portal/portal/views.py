import os
import pickle
import numpy as np
import pandas as pd

from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from malaria.models import Patient, DiagnosisQuestion, AdherenceQuestion, Report
from malaria.forms import PatientForm


CLASSIFIER_BASE = os.path.join(settings.BASE_DIR, 'malaria', 'classifiers')


class PatientAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PatientForm
    template_name = 'malaria/patient_form.html'
    success_message = 'Patient Created Successfully'


class PatientList(LoginRequiredMixin, ListView):
    model = Patient


class PatientDetail(LoginRequiredMixin, DetailView):
    model = Patient

class TrainingData(LoginRequiredMixin, TemplateView):
    template_name = "portal/training_data.html"
    
class Diagnosis(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        questions = DiagnosisQuestion.objects.all()
        patients = Patient.objects.all()
        context = {
            'questions': questions,
            'patients': patients,
        }
        return render(request, 'portal/diagnosis.html', context)

    def post(self, request, *args, **kwargs):
        patient_id = int(request.POST.get('patient'))
        patient = Patient.objects.get(id=patient_id)
        request_count = len(request.POST)-2
        choices = [int(request.POST.get('choice'+str(q+1))) for q in range(request_count)]
        print(choices)

        pickle_in = open(os.path.join(CLASSIFIER_BASE, 'malaria_prediction.pkl'), 'rb')
        clf_malaria = pickle.load(pickle_in)
        # answers = pd.DataFrame([[0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0]])
        answers = pd.DataFrame([choices])
        result = clf_malaria.predict(answers)
        print('Severe Malaria', result)
        possible_results = ['YES', 'NO']
        if result in possible_results:
            Report.objects.create(
                patient=patient,
                has_malaria=True if result == ['YES'] else False
            )
            messages.success(request, "Diagnosis Completed")
            return redirect(patient)
        messages.error(request, "Something went wrong!")
        return render(request, 'portal/diagnosis.html', {})


class AdherenceTest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        questions = AdherenceQuestion.objects.all()
        report_id = kwargs.get('pk')
        report = Report.objects.get(id=report_id)
        context = {
            'questions': questions,
            'patient': report.patient,
        }
        return render(request, 'portal/adherence.html', context)
    
    def post(self, request, *args, **kwargs):
        report_id = kwargs.get('pk')
        report = Report.objects.get(id=report_id)
        request_count = len(request.POST)-1
        choices = [int(request.POST.get('choice'+str(q+1))) for q in range(request_count)]
        print(choices)

        pickle_in = open(os.path.join(CLASSIFIER_BASE, 'adherence_prediction.pkl'), 'rb')
        clf_adh = pickle.load(pickle_in)
        # answers = pd.DataFrame([[0, 0, 0, 0, 1, 0, 1, 1, 1, 1]])
        answers = pd.DataFrame([choices])
        result = clf_adh.predict(answers)
        print('Adhered', result)
        possible_results = ['YES', 'NO']
        if result in possible_results:
            report.adhered_to_treatment = True if result == ['YES'] else False
            report.save()
            messages.success(request, "Adherence Test Completed")
            return redirect(report.patient)
        messages.error(request, "Something went wrong!")
        return render(request, 'portal/adherence.html', {})




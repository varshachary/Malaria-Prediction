from django.db import models
from django.shortcuts import reverse

class Patient(models.Model):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    full_name       = models.CharField(max_length=30)
    gender          = models.CharField(choices=GENDER_CHOICES, max_length=1)
    date_of_birth   = models.DateField()
    registered_on   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('portal:patient_detail', kwargs={'pk': self.pk})


class Report(models.Model):
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE)
    has_malaria         = models.NullBooleanField()
    adhered_to_treatment = models.NullBooleanField()
    generated_on        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.full_name
    
    class Meta:
        ordering = ["-generated_on"]


class DiagnosisQuestion(models.Model):
    question_text       = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ["id"]



class AdherenceQuestion(models.Model):
    question_text   = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text
    
    class Meta:
        ordering = ["id"]
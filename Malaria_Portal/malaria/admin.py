from django.contrib import admin

from .models import Patient, Report, DiagnosisQuestion, AdherenceQuestion


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name',)

admin.site.register(Patient, PatientAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'generated_on')

admin.site.register(Report, ReportAdmin)


admin.site.register(DiagnosisQuestion)
admin.site.register(AdherenceQuestion)

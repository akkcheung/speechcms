from django.contrib import admin

from .models import Applicant, LanguageCompetence, ProfessionalQualification, ProfessionalRecognition, WorkExperience

# Register your models here.
admin.site.register(Applicant)
admin.site.register(LanguageCompetence)
admin.site.register(ProfessionalQualification)
admin.site.register(ProfessionalRecognition)
admin.site.register(WorkExperience)

from django.contrib import admin

#from .models import Applicant, LanguageCompetence, ProfessionalQualification, ProfessionalRecognition, WorkExperience, News, Page, Fee
from .models import LanguageCompetence, ProfessionalQualification, ProfessionalRecognition, WorkExperience, News, Page, Fee

# Register your models here.
#admin.site.register(Applicant)
admin.site.register(LanguageCompetence)
admin.site.register(ProfessionalQualification)
admin.site.register(ProfessionalRecognition)
admin.site.register(WorkExperience)

admin.site.register(News)
admin.site.register(Page)

admin.site.register(Fee)

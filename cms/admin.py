from django.contrib import admin
from django.contrib.auth.models import Permission

#from .models import Applicant, LanguageCompetence, ProfessionalQualification, ProfessionalRecognition, WorkExperience, News, Page, Fee
from .models import LanguageCompetence, ProfessionalQualification, ProfessionalRecognition, WorkExperience, News, Page, Fee, PaymentHistory

# Register your models here.
admin.site.register(Permission)

#admin.site.register(Applicant)
admin.site.register(LanguageCompetence)
#admin.site.register(ProfessionalQualification)
#admin.site.register(ProfessionalRecognition)
#admin.site.register(WorkExperience)

#admin.site.register(News)
#admin.site.register(Page)

admin.site.register(Fee)

class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'currency', 'amount', 'user')
    list_display_links = ('date',)
    search_fields = ('user',)
    list_per_page = 25

admin.site.register(PaymentHistory,PaymentHistoryAdmin)

class ProfessionalQualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'degree_name_relevant_to_speech_therapy', 'english_translation_of_degree_name', 'university_name',  'user')
    list_display_links = ('degree_name_relevant_to_speech_therapy',)
    search_fields = ('user',)
    list_per_page = 25

admin.site.register(ProfessionalQualification,ProfessionalQualificationAdmin)

class ProfessionalRecognitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_name', 'organization_name', 'membership_type',  'expiry_date', 'user')
    list_display_links = ('id',)
    search_fields = ('user',)
    list_per_page = 25

admin.site.register(ProfessionalRecognition,ProfessionalRecognitionAdmin)

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employer_name', 'job_title', 'start_date',  'end_date', 'user')
    list_display_links = ('id',)
    search_fields = ('user',)
    list_per_page = 25

admin.site.register(WorkExperience, WorkExperienceAdmin)

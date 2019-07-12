from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views import generic
from django.forms.models import  modelformset_factory, inlineformset_factory


from .models import Applicant, WorkExperience, ProfessionalQualification, ProfessionalRecognition
from .forms import ApplicantForm, LanguageCompetenceForm, WorkExperienceForm, ApplicantFormShort, ProfessionalQualificationForm, ProfessionalQualificationFormSetHelper, WorkExperienceFormSetHelper, ProfessionalRecognitionForm, ProfessionalRecognitionFormSetHelper


# Create your views here.
class ApplicantCreate(CreateView):
    model = Applicant
    #fields = ('last_name', 'first_name', 'email')
    form_class = ApplicantForm
    template_name = 'cms/application_form.html'

class ApplicantUpdate(UpdateView):
    model = Applicant
    fields = ['last_name', 'first_name', 'email']

class ApplicantDetailView(generic.DetailView):
    model = Applicant

def Applicant_edit(request):
    if request.method == 'POST':
        applicant_form = ApplicantFormShort(request.POST)
        work_experience_form = WorkExperienceForm(request.POST)

        if all([applicant_form.is_valid(), work_experience_form.is_valid()]):
            #applicant = applicant_form.save()
            #work_experience = work_experience_form.save()

            work_experience = work_experience_form.save(commit=False)
            work_experience.applicant = applicant_form.save()
            work_experience.save()

            return redirect(user)

    else:
        applicant_form = ApplicantFormShort()
        work_experience_form = WorkExperienceForm()

    return render(request, 'cms/application_form_full.html', {
        'applicant_form': applicant_form,
        'work_experience_form': work_experience_form,
    })

def Applicant_formset_create(request):
    ProfessionalQualificationFormset = modelformset_factory(ProfessionalQualification, form=ProfessionalQualificationForm, max_num=3, extra=3)
    ProfessionalRecognitionFormset = modelformset_factory(ProfessionalRecognition, form=ProfessionalRecognitionForm, max_num=3, extra=3)
    WorkExpFormset = modelformset_factory(WorkExperience, form=WorkExperienceForm,  max_num=3, extra=3)

    if request.method == 'POST':
        applicant_form = ApplicantFormShort(request.POST)
        language_form = LanguageCompetenceForm(request.POST)

        #formset = WorkExperienceFormSet(request.POST, request.FILES)
        formsetPQ = ProfessionalQualificationFormset(request.POST, request.FILES)
        formsetPR = ProfessionalRecognitionFormset(request.POST, request.FILES)
        formsetWE = WorkExpFormset(request.POST, request.FILES)

        if all([applicant_form.is_valid(), language_form.is_valid(), formsetPQ.is_valid(), formsetWE.is_valid()]):
            forms_pq = formsetPQ.save(commit=False)
            forms_pr = formsetPR.save(commit=False)
            forms_we = formsetWE.save(commit=False)

            applicant_save = applicant_form.save()

            language = language_form.save(commit=False)
            language.applicant = applicant_save
            language.save()

            for form in forms_pq:
                form.applicant = applicant_save
                form.save()

            for form in forms_pr:
                form.applicant = applicant_save
                form.save()

            for form in forms_we:
                #form.applicant = applicant_form.save()
                form.applicant = applicant_save
                form.save()

            return redirect(user)

    else :
        applicant_form = ApplicantFormShort()
        language_form = LanguageCompetenceForm()
        formsetPQ = ProfessionalQualificationFormset(queryset=ProfessionalQualification.objects.filter(applicant=0))
        formsetPR = ProfessionalRecognitionFormset(queryset=ProfessionalRecognition.objects.filter(applicant=0))
        #formset = WorkExperienceFormSet()
        formsetWE = WorkExpFormset(queryset=WorkExperience.objects.filter(applicant=0))


    return render(request, 'cms/application_formset.html', {
            'applicant_form': applicant_form,
            'language_form': language_form,
            'professional_qualification_formset': formsetPQ,
            'professional_recognition_formset': formsetPR,
            'work_experience_formset': formsetWE,
            'helper': ProfessionalQualificationFormSetHelper,
            'helper_we' : WorkExperienceFormSetHelper,
            'helper_pr' : ProfessionalRecognitionFormSetHelper,
    })

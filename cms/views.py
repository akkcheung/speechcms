from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from django.forms.models import  modelformset_factory, inlineformset_factory
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.conf import settings
from django.views.generic.base import TemplateView

import stripe
import datetime

#from .models import Applicant, WorkExperience, ProfessionalQualification, ProfessionalRecognition, News, Page, Fee, PaymentHistory

from .models import WorkExperience, ProfessionalQualification, ProfessionalRecognition, News, Page, Fee, PaymentHistory

#from .forms import ApplicantForm, LanguageCompetenceForm, WorkExperienceForm, ApplicantFormShort, ProfessionalQualificationForm, ProfessionalQualificationFormSetHelper, WorkExperienceFormSetHelper, ProfessionalRecognitionForm, ProfessionalRecognitionFormSetHelper, DocumentForm, NewsForm, PageForm, SignUpForm, PersonDetailForm
from .forms import LanguageCompetenceForm, WorkExperienceForm, ProfessionalQualificationForm,  ProfessionalRecognitionForm,  DocumentForm, NewsForm, PageForm, SignUpForm, PersonDetailForm, ProfessionalQualificationFormset

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
'''
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
'''

'''
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
'''

'''
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

        document_form = DocumentForm(request.POST, request.FILES)

        if all([applicant_form.is_valid(), language_form.is_valid(), formsetPQ.is_valid(), formsetWE.is_valid(), document_form.is_valid()]):
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

            #document = document_form.save(commit=False)
            #document.applicant = applicant_save
            #document.save()

            return redirect(user)

    else :
        applicant_form = ApplicantFormShort()
        language_form = LanguageCompetenceForm()
        formsetPQ = ProfessionalQualificationFormset(queryset=ProfessionalQualification.objects.filter(applicant=0))
        formsetPR = ProfessionalRecognitionFormset(queryset=ProfessionalRecognition.objects.filter(applicant=0))
        #formset = WorkExperienceFormSet()
        formsetWE = WorkExpFormset(queryset=WorkExperience.objects.filter(applicant=0))
        document_form = DocumentForm()

    return render(request, 'cms/application_formset.html', {
            'applicant_form': applicant_form,
            'language_form': language_form,
            'professional_qualification_formset': formsetPQ,
            'professional_recognition_formset': formsetPR,
            'work_experience_formset': formsetWE,
            'helper': ProfessionalQualificationFormSetHelper,
            'helper_we' : WorkExperienceFormSetHelper,
            'helper_pr' : ProfessionalRecognitionFormSetHelper,
            'document_form' : document_form,
    })
'''

def index(request):
    #return HttpResponse('hello from index')
    context = {}
    return render(request, 'cms/index.html', context)

def about(request):
   return HttpResponse('hello from about')

def contact(request):
   #return HttpResponse('hello from contact')
   context = {}
   return render(request, 'cms/contact.html', context)

def tinymce(request):
   #return HttpResponse('hello from contact')

   news_form = NewsForm()
   context = {
        'form': news_form,
   }

   return render(request, 'cms/tinymce.html', context)

class NewsCreate(CreateView):
    model = News
    #fields = '__all__'
    form_class = NewsForm


class NewsUpdate(UpdateView):
    model = News
    #fields = ['publish_date', 'content', 'is_publish']
    form_class = NewsForm

class NewsDelete(DeleteView):
    model = News
    success_url = reverse_lazy('news')

class PageCreate(CreateView):
    model = Page
    #fields = '__all__'
    form_class = PageForm


class PageUpdate(UpdateView):
    model = Page
    #fields = ['publish_date', 'content', 'is_publish']
    form_class = PageForm

class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('page')

def PageShow(request):
    if request.method == 'GET':
        #news_form = NewsForm()
        context = {
           #'form': news_form,
        }

    return render(request, 'cms/tinymce.html', context)

def SignUp(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

class HomeView(TemplateView):
    template_name = 'home.html'
    # fee = get_object_or_404(Fee, description='Annual Subscription Fee')

    #def get_queryset(self):
    #    qs = super().get_queryset() # 调用父类方法
    #    return qs.filter(author = self.request.user).order_by('-pub_date')

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY

        fee_list = Fee.objects.filter(description = 'Annual Subscription Fee')
        #fee = fee_list.order_by('-date_effective')[0]
        context['fee'] = fee_list.order_by('-date_effective')[0]

        fee = fee_list.order_by('-date_effective')[0]
        context['amount'] = fee.amount * 100

        return context


def charge(request):
    if request.method == 'POST':

        context = {
            #'form': news_form,
            'result' : '' ,
        }

        try:
            charge = stripe.Charge.create(
                #amount=500,
                amount=request.POST['amount'],
                #currency='usd',
                currency='hkd',
                #description='A Django charge',
                description=request.POST['description'],
                source=request.POST['stripeToken']
            )

            p = PaymentHistory(date=datetime.date.today(), amount=request.POST['fee_amount'], currency='HKD', description=request.POST['description'], user=request.user)

            p.save()

            context['result'] = "<h2>Thanks, you paid <strong>$" + request.POST['fee_amount'] + "</strong></h2>"
        except stripe.error.StripeError as e:
            context['result'] = "<h2>Something goes wrong</h2>"
        except Exception as e:
            #print '%s (%s)' % (e.message, type(e))
            print (type(e))
            print (e)
            context['result'] = "<h2>Something goes wrong</h2>"

        #return render(request, 'charge.html')
        return render(request, 'charge.html', context)

def Applicant_form_create(request):
    user=request.user
    #ProfessionalQualificationFormset = modelformset_factory(ProfessionalQualification, form=ProfessionalQualificationForm, max_num=3, extra=3)


    if request.method == 'POST':
        p_form = PersonDetailForm(request.POST)
        lc_form = LanguageCompetenceForm(request.POST)
        formset_pq = ProfessionalQualificationFormset(request.POST)
        form_doc = DocumentForm(request.POST, request.FILES)

        #print (request.POST['country_of_birth'])

        #if p_form.is_valid():
        if all([p_form.is_valid(), lc_form.is_valid(), formset_pq.is_valid(), form_doc.is_valid(),]):
            #form.save()
            personDetail = p_form.save(commit=False)
            personDetail.user = user
            personDetail.save()

            lc = lc_form.save(commit=False)
            lc.user = user
            lc.save()

            #forms_pq = formset_pq.save(commit=False)
            #for form in forms_pq:
            for form in formset_pq:
                pq = form.save(commit=False)
                pq.user = user
                pq.save()

            document = form_doc.save(commit=False)
            document.user = user
            document.save()

            return redirect('my-profile')

    else :
        p_form = PersonDetailForm()
        lc_form = LanguageCompetenceForm()
        #formset_pq = ProfessionalQualificationFormset(queryset=ProfessionalQualification.objects.filter(user=0))
        formset_pq = ProfessionalQualificationFormset()
        form_doc = DocumentForm()

    context = {
        'p_form' : p_form,
        'user' : user,
        'lc_form' : lc_form,
        'formset_pq' : formset_pq,
        'form_doc' : form_doc,
    }

    return render(request, 'cms/assessment_form.html', context)

'''
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
'''

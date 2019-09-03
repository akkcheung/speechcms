from django.http import HttpResponse, FileResponse
from django.forms.models import  modelformset_factory, inlineformset_factory, model_to_dict
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.conf import settings
from django.views.generic.base import TemplateView

#from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

import stripe
import datetime
import json

#from .models import Applicant, WorkExperience, ProfessionalQualification, ProfessionalRecognition, News, Page, Fee, PaymentHistory

from .models import WorkExperience, ProfessionalQualification, ProfessionalRecognition, News, Page, Fee, PaymentHistory, PersonDetail, LanguageCompetence, Document

#from .forms import ApplicantForm, LanguageCompetenceForm, WorkExperienceForm, ApplicantFormShort, ProfessionalQualificationForm, ProfessionalQualificationFormSetHelper, WorkExperienceFormSetHelper, ProfessionalRecognitionForm, ProfessionalRecognitionFormSetHelper, DocumentForm, NewsForm, PageForm, SignUpForm, PersonDetailForm
from .forms import LanguageCompetenceForm, WorkExperienceForm, ProfessionalQualificationForm,  ProfessionalRecognitionForm,  DocumentForm, NewsForm, PageForm, SignUpForm, PersonDetailForm, ProfessionalQualificationFormset, ProfessionalRecognitionFormset, WorkExperienceFormset

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def index(request):
    #return HttpResponse('hello from index')

    #context = {}
    #return render(request, 'cms/index.html', context)

    response = redirect('/cms/page/news')
    return response

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


#class PageCreate(CreateView):
class PageCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'is_staff'
    model = Page
    #fields = '__all__'
    form_class = PageForm


class PageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    model = Page
    #fields = ['publish_date', 'content', 'is_publish']
    form_class = PageForm


class PageDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_staff'
    model = Page
    success_url = reverse_lazy('page')

def PageShow(request, url_path):
    if request.method == 'GET':
        #news_form = NewsForm()

        page_list = Page.objects.filter(url_path = url_path)
        page = page_list[0]

        context = {
           'page': page,
        }

        #context['page'] = page

    #return render(request, 'cms/tinymce.html', context)
    return render(request, 'cms/page_show.html', context)

def SignUp(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            my_group = Group.objects.get(name='hkist_member')
            my_group.user_set.add(user)
            login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    query_pk_and_slug = 'email'
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

        personDetail_list =  PersonDetail.objects.filter(user= self.request.user)

        context['amount'] = fee.amount * 100
        context['personDetail_list'] = personDetail_list

        return context

def home_view(request, username):
    if request.method == 'GET':
        #news_form = NewsForm()

        user_list = User.objects.filter(username = username)
        user = user_list[0]

        fee_list = Fee.objects.filter(description = 'Annual Subscription Fee')
        fee = fee_list.order_by('-date_effective')[0]

        context = {
           'key': settings.STRIPE_PUBLISHABLE_KEY,
           'member': user,
           'fee': fee,
        }

    return render(request, 'cms/home_view.html', context)


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

def Assessment_form_create(request):
    user=request.user
    #ProfessionalQualificationFormset = modelformset_factory(ProfessionalQualification, form=ProfessionalQualificationForm, max_num=3, extra=3)


    if request.method == 'POST':
        p_form = PersonDetailForm(request.POST)
        lc_form = LanguageCompetenceForm(request.POST)
        formset_pq = ProfessionalQualificationFormset(request.POST)
        form_doc = DocumentForm(request.POST, request.FILES)

        formset_pr = ProfessionalRecognitionFormset(request.POST,  prefix='pr')
        form_doc_a = DocumentForm(request.POST, request.FILES, prefix="doc-pr")

        formset_wk = WorkExperienceFormset(request.POST, prefix='wk')
        form_doc_b = DocumentForm(request.POST, request.FILES, prefix="doc-wk")

        #print (request.POST['country_of_birth'])

        #if p_form.is_valid():
        if all([ p_form.is_valid(), lc_form.is_valid(), formset_pq.is_valid(), form_doc.is_valid(), formset_pr.is_valid(), form_doc_a.is_valid(), formset_wk.is_valid(), form_doc_b.is_valid(), ]):
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
                #if pq.degree_name_relevant_to_speech_therapy == '' and  pq.university_name == '' and pq.english_translation_of_degree_name == '' and pq.english_university_name == '' :
                #    continue
                #else :
                #    pq.user = user
                #    pq.save()
                pq.user = user
                pq.save()

            document = form_doc.save(commit=False)
            document.user = user
            document.save()

            for form in formset_pr:
                pr = form.save(commit=False)
                #if pr.country_name == '' and pr.organization_name == '' and pr.membership_type == '' :
                #    continue
                #else :
                #    pr.user = user
                #    pr.save()
                pr.user = user
                pr.save()

            document = form_doc_a.save(commit=False)
            document.user = user
            document.save()

            for form in formset_wk:
                wk = form.save(commit=False)
                #if wk.employer_name == '' and wk.job_title == ''  :
                #    continue
                #else :
                #    wk.user = user
                #    wk.save()
                wk.user = user
                wk.save()

            document = form_doc_b.save(commit=False)
            document.user = user
            document.save()

            return redirect('my-profile')

    else :
        p_form = PersonDetailForm()
        lc_form = LanguageCompetenceForm()
        #formset_pq = ProfessionalQualificationFormset(queryset=ProfessionalQualification.objects.filter(user=0))
        formset_pq = ProfessionalQualificationFormset(queryset=ProfessionalQualification.objects.filter(user=user))
        form_doc = DocumentForm()

        formset_pr = ProfessionalRecognitionFormset(queryset=ProfessionalRecognition.objects.filter(user=user) , prefix='pr')
        form_doc_a = DocumentForm(prefix="doc-pr")

        formset_wk = WorkExperienceFormset(queryset=WorkExperience.objects.filter(user=user), prefix='wk')
        form_doc_b = DocumentForm(prefix="doc-wk")

    context = {
        'p_form' : p_form,
        'user' : user,
        'lc_form' : lc_form,
        'formset_pq' : formset_pq,
        'form_doc' : form_doc,
        'formset_pr' : formset_pr,
        'form_doc_a': form_doc_a,
        'formset_wk' : formset_wk,
        'form_doc_b': form_doc_b,
    }

    #return render(request, 'cms/assessment_form.html', context)
    return render(request, 'cms/assessment_form_edit.html', context)

#def Assessment_form_edit(request):
def Assessment_form_edit(request, username='None'):

    user=request.user

    if user.is_staff :
        user = User.objects.filter(username=username).first()

    personDetail = PersonDetail.objects.filter(user=user).first()
    languageCompetence = LanguageCompetence.objects.filter(user=user).first()

    document_list = Document.objects.filter(user=user).order_by('id')
    #document = Document.objects.filter(user=user).order_by('id').first()

    document = document_list[0]
    document_a = document_list[1]
    document_b = document_list[2]

    if request.method == 'POST':
        p_form = PersonDetailForm(request.POST, instance=personDetail)
        lc_form = LanguageCompetenceForm(request.POST,  instance=languageCompetence)
        formset_pq = ProfessionalQualificationFormset(request.POST)
        form_doc = DocumentForm(request.POST, request.FILES, instance=document)

        formset_pr = ProfessionalRecognitionFormset(request.POST, prefix='pr')
        form_doc_a = DocumentForm(request.POST, request.FILES, instance=document_a, prefix="doc-pr")

        formset_wk = WorkExperienceFormset(request.POST, prefix='wk')
        form_doc_b = DocumentForm(request.POST, request.FILES, instance=document_b, prefix="doc-wk")

        #if all([ p_form.is_valid(), lc_form.is_valid(), formset_pq.is_valid(), form_doc.is_valid(), ]):
        if all([ p_form.is_valid(), lc_form.is_valid(), formset_pq.is_valid(),form_doc.is_valid(), formset_pr.is_valid(), form_doc_a.is_valid(), formset_wk.is_valid(), form_doc_b.is_valid() ]):
            personDetail = p_form.save(commit=False)
            #personDetail.user = user
            personDetail.save()

            lc = lc_form.save(commit=False)
            lc.save()

            for form in formset_pq:
                pq = form.save(commit=False)
                if pq.degree_name_relevant_to_speech_therapy == '' and  pq.university_name == '' and pq.english_translation_of_degree_name == '' and pq.english_university_name == '' :
                    continue
                else :
                    pq.user = user
                    pq.save()

            document = form_doc.save(commit=False)
            document.user = user
            document.save()

            for form in formset_pr:
                pr = form.save(commit=False)
                if pr.country_name == '' and pr.organization_name == '' and pr.membership_type == '' :
                    continue
                else :
                    pr.user = user
                    pr.save()

            document_a = form_doc_a.save(commit=False)
            document_a.user = user
            document_a.save()

            for form in formset_wk:
                wk = form.save(commit=False)
                if wk.employer_name == '' and wk.job_title == ''  :
                    continue
                else :
                    wk.user = user
                    wk.save()

            document_b = form_doc_b.save(commit=False)
            document_b.user = user
            document_b.save()


            return redirect('my-profile')

    else:
        p_form =  PersonDetailForm(instance=personDetail)
        lc_form = LanguageCompetenceForm(instance=languageCompetence)
        formset_pq = ProfessionalQualificationFormset(queryset=ProfessionalQualification.objects.filter(user=user))
        form_doc = DocumentForm(instance=document)

        formset_pr = ProfessionalRecognitionFormset(queryset=ProfessionalRecognition.objects.filter(user=user) , prefix='pr')
        form_doc_a = DocumentForm(instance=document_a, prefix="doc-pr")

        formset_wk = WorkExperienceFormset(queryset=WorkExperience.objects.filter(user=user), prefix='wk')
        form_doc_b = DocumentForm(instance=document_b, prefix="doc-wk")

    context = {
        'p_form' : p_form,
        'lc_form' : lc_form,
        'formset_pq' : formset_pq,
        'form_doc' : form_doc,
        'formset_pr' : formset_pr,
        'form_doc_a' : form_doc_a,
        'formset_wk' : formset_wk,
        'form_doc_b': form_doc_b,
        'user': user,
    }

    return render(request, 'cms/assessment_form_edit.html', context)

#class RegisterUserListView(LoginRequiredMixin,generic.ListView):
class RegisterUserListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'is_staff'
    model : User
    template_name = 'cms/register_user_list.html'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(groups__name__in=['hkist_member']).order_by('username')


#class RegistrantListView(PermissionRequiredMixin, generic.ListView):
class RegistrantListView(LoginRequiredMixin, generic.ListView):
    #permission_required = 'is_staff'
    model : User
    template_name = 'cms/registrant_list.html'
    paginate_by = 10
    context_object_name = 'registrant_list'

    def get_queryset(self):
        return User.objects.filter(groups__name__in=['hkist_member']).order_by('username')

class PaymentHistoryListView(LoginRequiredMixin, generic.ListView):
    #permission_required = 'is_staff'
    model : PaymentHistory
    template_name = 'cms/payment_history_list.html'
    paginate_by = 10
    context_object_name = 'payment_history_list'

    def get_queryset(self):
        return PaymentHistory.objects.filter(user=self.request.user).order_by('-date')

@login_required()
def serve_protected_document(request, file):

    print ('file')
    print (file)
    #document = get_object_or_404(Document, document="media/documents/" + file)
    document = get_object_or_404(Document, document="documents/" + file)

    # Split the elements of the path
    #path, file_name = os.path.split(file)

    #response = FileResponse(document.file,)
    response = FileResponse(document.document,)
    #response["Content-Disposition"] = "attachment; filename=" + file_name
    response["Content-Disposition"] = "attachment; filename=" + file

    return response

'''
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
'''

from django import forms
from django.forms import formset_factory, modelformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

#from .models import Applicant, LanguageCompetence, WorkExperience, ProfessionalQualification, ProfessionalRecognition, Document, News, Page, PersonDetail
from .models import LanguageCompetence, WorkExperience, ProfessionalQualification, ProfessionalRecognition, Document, News, Page, PersonDetail

#from tinymce.widgets import TinyMCE
from tinymce import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False
'''
class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('last_name', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save application'))
'''

'''
class ApplicantFormShort(forms.ModelForm):
    last_name = forms.CharField(label='Last Name', max_length=100)

    class Meta:
        model = Applicant
        fields = ('title', 'last_name', 'first_name', 'date_of_birth', 'country_of_birth', 'address', 'phone', 'email')
'''

class LanguageCompetenceForm(forms.ModelForm):
    dominant_language_other = forms.CharField(label='Others', max_length=100, required=False)
    language_in_which_speech_therapy_training_was_conducted_other = forms.CharField(label='Others', max_length=100, required=False)
    language_to_provide_speech_therapy_other = forms.CharField(label='Others', max_length=100, required=False)

    class Meta:
        model = LanguageCompetence
        #fields = ('dominant_language', 'dominant_language_other', 'language_in_which_speech_therapy_training_was_conducted','language_in_which_speech_therapy_training_was_conducted_other', 'language_to_provide_speech_therapy', 'language_to_provide_speech_therapy_other')
        exclude = { 'user', }

class ProfessionalQualificationForm(forms.ModelForm):
    degree_name_relevant_to_speech_therapy = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Degree Name')
    english_translation_of_degree_name  = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))

    graduation_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    country_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), required=False)

    class Meta:
        model = ProfessionalQualification
        #fields = ('degree_name_relevant_to_speech_therapy', 'english_translation_of_degree_name', 'university_name', 'english_university_name', 'country_name', 'language_of_instruction', 'graduation_date', 'qualifiation_framework_level')
        exclude = { 'user', }

#ProfessionalQualificationFormset = formset_factory(ProfessionalQualificationForm, max_num=3, extra=3)
#ProfessionalQualificationFormset = modelformset_factory(ProfessionalQualification,  exclude = { 'user', }, max_num=3, extra=3)
#ProfessionalQualificationFormset = modelformset_factory(form=ProfessionalQualificationForm, model=ProfessionalQualification, max_num=3, extra=3)
ProfessionalQualificationFormset = modelformset_factory(form=ProfessionalQualificationForm, model=ProfessionalQualification, max_num=3, extra=1)

class ProfessionalRecognitionForm(forms.ModelForm):

    expiry_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = ProfessionalRecognition
        #fields = ('country_name', 'organization_name', 'membership_type', 'expiry_date')
        exclude = { 'user', }

#ProfessionalRecognitionFormset = formset_factory(ProfessionalRecognitionForm, max_num=2, extra=2)
#ProfessionalRecognitionFormset = modelformset_factory(ProfessionalRecognition,  exclude = {'user',}, max_num=2, extra=2)
ProfessionalRecognitionFormset = modelformset_factory(form=ProfessionalRecognitionForm, model=ProfessionalRecognition, max_num=2, extra=1)

class WorkExperienceForm(forms.ModelForm):

    start_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    end_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = WorkExperience
        #fields = ('employer_name', 'job_title', 'start_date', 'end_date')
        exclude = { 'user', }

#WorkExperienceFormset = formset_factory(WorkExperienceForm, max_num=3, extra=3)
WorkExperienceFormset = modelformset_factory(form=WorkExperienceForm, model=WorkExperience, max_num=3, extra=1)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class NewsForm(forms.ModelForm):
    #content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 80, 'rows': 30}
        )
    )
    publish_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = News
        #fields = ('url_path', 'publish_date', 'content', 'is_publish')
        # fields = ('publish_date', 'content', 'is_publish')
        fields = '__all__'

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
    '''

class PageForm(forms.ModelForm):
    content = forms.CharField(
        #widget=TinyMCE(
        #    attrs={'cols': 80, 'rows': 30}
        #)
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 80, 'rows': 30}
        )
    )
    publish_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Page
        #fields = ('url_path', 'publish_date', 'content', 'is_publish')
        #fields = ('publish_date', 'content', 'is_publish')
        fields = '__all__'

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
    '''

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class PersonDetailForm(forms.ModelForm):

    date_of_birth = forms.DateField(

        widget=forms.TextInput(
            attrs={'type': 'date'}
        )

        #widget=forms.SelectDateWidget(years, months, empty_label)
    )

    class Meta:
        model = PersonDetail
        #fields = ('last_name', 'first_name', 'email')
        #fields = '__all__'
        exclude = { 'user', }

    #def __init__(self, *args, **kwargs):
    #    user = kwargs.pop('user','')
    #    super(PersonDetailForm, self).__init__(*args, **kwargs)

from django import forms
from django.forms import formset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

from .models import Applicant, LanguageCompetence, WorkExperience, ProfessionalQualification, ProfessionalRecognition

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('last_name', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save application'))

class ApplicantFormShort(forms.ModelForm):
    last_name = forms.CharField(label='Last Name', max_length=100)

    class Meta:
        model = Applicant
        fields = ('title', 'last_name', 'first_name', 'date_of_birth', 'country_of_birth', 'address', 'phone', 'email')

class LanguageCompetenceForm(forms.ModelForm):
    dominant_language_other = forms.CharField(label='Others', max_length=100)
    language_in_which_speech_therapy_training_was_conducted_other = forms.CharField(label='Others', max_length=100)
    language_to_provide_speech_therapy_other = forms.CharField(label='Others', max_length=100)

    class Meta:
        model = LanguageCompetence
        fields = ('dominant_language', 'dominant_language_other', 'language_in_which_speech_therapy_training_was_conducted','language_in_which_speech_therapy_training_was_conducted_other',
        'language_to_provide_speech_therapy', 'language_to_provide_speech_therapy_other')

class ProfessionalQualificationForm(forms.ModelForm):
    degree_name_relevant_to_speech_therapy = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label='Degree Name')
    english_translation_of_degree_name  = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))

    class Meta:
        model = ProfessionalQualification
        fields = ('degree_name_relevant_to_speech_therapy', 'english_translation_of_degree_name', 'university_name', 'english_university_name', 'country_name', 'language_of_instruction', 'graduation_date', 'qualifiation_framework_level')

class ProfessionalRecognitionForm(forms.ModelForm):
    class Meta:
        model = ProfessionalRecognition
        fields = ('country_name', 'organization_name', 'membership_type', 'expiry_date')


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ('employer_name', 'job_title', 'start_date', 'end_date')

class ProfessionalQualificationFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProfessionalQualificationFormSetHelper, self).__init__(*args, **kwargs)
        #self.form_method = 'post'
        self.layout = Layout(
            Row(
                Column('degree_name_relevant_to_speech_therapy', css_class='form-group col-md-3 mb-0'),
                Column('english_translation_of_degree_name', css_class='form-group col-md-3 mb-0'),
                Column('university_name', css_class='form-group col-md-3 mb-0'),
                Column('english_university_name', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('country_name', css_class='form-group col-md-3 mb-0'),
                Column('language_of_instruction', css_class='form-group col-md-3 mb-0'),
                Column('graduation_date', css_class='form-group col-md-3 mb-0'),
                Column('qualifiation_framework_level', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            )
        )
        self.render_required_fields = True

class ProfessionalRecognitionFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProfessionalRecognitionFormSetHelper, self).__init__(*args, **kwargs)
        #self.form_method = 'post'
        self.layout = Layout(
            Row(
                Column('country_name', css_class='form-group col-md-3 mb-0'),
                Column('organization_name', css_class='form-group col-md-3 mb-0'),
                Column('membership_type', css_class='form-group col-md-3 mb-0'),
                Column('expiry_date', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            )
        )
        self.render_required_fields = True

class WorkExperienceFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(WorkExperienceFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Row(
                Column('employer_name', css_class='form-group col-md-4 mb-0'),
                Column('job_title', css_class='form-group col-md-4 mb-0'),
                Column('start_date', css_class='form-group col-md-2 mb-0'),
                Column('end_date', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            )
        )
        self.render_required_fields = True

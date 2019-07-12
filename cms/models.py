from django.db import models
from django.urls import reverse

import datetime

# Create your models here.
class Applicant(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=False, default=datetime.date.today)
    country_of_birth = models.CharField(max_length=10, default='HK')
    address = models.CharField(max_length=300, default='')
    phone = models.CharField(max_length=8, default='')
    email = models.EmailField(blank=False)

    TITLE = (
        ('Prof.', 'Prof.'),
        ('Dr.', 'Dr.'),
        ('Mr.', 'Mr.'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        )

    title = models.CharField(
        max_length=4,
        choices=TITLE,
        blank=True,
        default='',
        #help_text='Dominant Language',
    )

    #declare_and_consent =models.BooleanField()

    #work_experience = models.ForeignKey('WorkExperience', on_delete=models.SET_NULL, null=True)

    #professional_recognition = models.ForeignKey('ProfessionalRecognition', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('applicant-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.email

class LanguageCompetence(models.Model):

    LANG = (
        ('C', 'Cantonese'),
        ('E', 'English'),
        ('P', 'Putonghua'),
        ('O', 'Others'),
    )

    dominant_language = models.CharField(
        max_length=1,
        choices=LANG,
        blank=True,
        default='',
        #help_text='Dominant Language',
    )

    dominant_language_other = models.CharField(max_length=100, default='')

    language_in_which_speech_therapy_training_was_conducted = models.CharField(
        max_length=1,
        choices=LANG,
        blank=True,
        default='',
        #help_text='Dominant Language',
    )

    language_in_which_speech_therapy_training_was_conducted_other = models.CharField(max_length=100, default='')

    language_to_provide_speech_therapy = models.CharField(
        max_length=1,
        choices=LANG,
        blank=True,
        default='',
        #help_text='Dominant Language',
    )

    language_to_provide_speech_therapy_other = models.CharField(max_length=100, default='')

    applicant = models.ForeignKey('Applicant', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.dominant_language

class ProfessionalQualification(models.Model):
    degree_name_relevant_to_speech_therapy = models.CharField(max_length=200)
    english_translation_of_degree_name = models.CharField(max_length=200)
    university_name = models.CharField(max_length=200)
    english_university_name = models.CharField(max_length=200)
    country_name = models.CharField(max_length=200)
    language_of_instruction = models.CharField(max_length=200)
    graduation_date = models.DateField(null=False, blank=False)
    qualifiation_framework_level = models.CharField(max_length=200)

    applicant = models.ForeignKey('Applicant', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.english_translation_of_degree_name

class ProfessionalRecognition(models.Model):
    country_name = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200)
    membership_type = models.CharField(max_length=200)
    expiry_date = models.DateField(null=False, blank=False)

    applicant = models.ForeignKey('Applicant', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.organization_name

class WorkExperience(models.Model):
    employer_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    applicant = models.ForeignKey('Applicant', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.job_title}'

#class Payment(models.Model):

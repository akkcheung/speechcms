from django.urls import path
from . import views


urlpatterns = []

urlpatterns += [
    path('applicant/create/', views.ApplicantCreate.as_view(), name='applicant_create'),
    path('applicant/<int:pk>/update/', views.ApplicantUpdate.as_view(), name='applicant_update'),
    #path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('applicant/<int:pk>', views.ApplicantDetailView.as_view(), name='applicant-detail'),
    path('application/new/', views.Applicant_edit, name='applicant_new'),
    path('application/create/', views.Applicant_formset_create, name='Applicant_formset_create'),
]

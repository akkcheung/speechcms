from django.urls import path, include
from django.conf import settings
#from django.conf.urls.static import static
from django.views.generic.base import TemplateView


from . import views
#from .filebrowser import site
#from filebrowser.sites import site


urlpatterns = []

urlpatterns += [
    #path('applicant/create/', views.ApplicantCreate.as_view(), name='applicant_create'),
    #path('applicant/<int:pk>/update/', views.ApplicantUpdate.as_view(), name='applicant_update'),
    #path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    #path('applicant/<int:pk>', views.ApplicantDetailView.as_view(), name='applicant-detail'),
    #path('application/new/', views.Applicant_edit, name='applicant_new'),
    #path('application/create/', views.Applicant_formset_create, name='Applicant_formset_create'),
]

urlpatterns += [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tinymce/', views.tinymce, name='tinymce'),
]

urlpatterns += [
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', views.NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', views.NewsDelete.as_view(), name='news_delete'),
]

urlpatterns += [
    path('page/create/', views.PageCreate.as_view(), name='page_create'),
    path('page/<int:pk>/update/', views.PageUpdate.as_view(), name='page_update'),
    path('page/<int:pk>/delete/', views.PageDelete.as_view(), name='page_delete'),
]

urlpatterns += [
    #path('governance', views.PageShow.as_view, name='page_show')
    path('signup/', views.SignUp, name='signup'),
]

urlpatterns += [
    #path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('my-profile/', views.HomeView.as_view(), name='my-profile'),
    path('charge/', views.charge, name='charge'),
    #path('members-register/', views.HomeView.as_view(), name='members-register'),
    path('assessment-form/', views.Applicant_form_create, name='assessment-form'),
]

#urlpatterns += [
#    url(r'^admin/content/file/', include(site.urls)),
#]

#if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
#    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )

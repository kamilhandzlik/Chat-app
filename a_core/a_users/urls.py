from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('edit/', views.profile_edit_view, name='profile_edit'),
    path('onboarding/', views.profile_edit_view, name='profile-onboarding'),
    path('@<username>/', views.profile_view, name='profile'),
    path('settings/', views.profile_settings_view, name="profile-settings"),
    path('emailchange/', views.profile_emailchange, name='profile-emailchange'),
    path('emailverify/', views.profile_emailverify, name='profile-emailverify'),
    path('delete/', views.profile_delete_view, name='profile-delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

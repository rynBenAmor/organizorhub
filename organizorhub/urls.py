
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)#check source code for template names
from leads.views import SignupView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('leads.urls')),  # Include the leads app's URLconf
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('agents/', include('agents.urls')),

    path('reset_password/', PasswordResetView.as_view(), name='reset_password'),#tip: django prio/defaults its own temp so explictly add your app temp dir in setting.py
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),#it comes with default url and name pattern
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),#both kwargs here are necessary
    path('password_resset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
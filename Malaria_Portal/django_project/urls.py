from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(
        template_name='home.html'
    ), name='home'),
    path('about/', TemplateView.as_view(
        template_name='about.html'
    ), name='about'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('portal/', include('portal.urls', namespace='portal')),
]

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^postTeams/$', views.postTeams),
    url(r'^postResults/$', views.postResults)
]
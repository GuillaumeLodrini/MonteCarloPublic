import main.views

from django.urls import path


urlpatterns = [
    path('', main.views.IndexTemplateView.as_view(), name='index'),
]

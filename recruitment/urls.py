from django.urls import path, include
from recruitment import views


urlpatterns = [
    path('', views.LoginPageView.as_view(), name='login'),
    path('applicationPage', views.ApplicationPage.as_view(), name='applicationPage'),
]

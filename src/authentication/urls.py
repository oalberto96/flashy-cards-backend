from django.conf.urls import url
from authentication import views

urlpatterns = [
    url("login", views.login, name="login")
]

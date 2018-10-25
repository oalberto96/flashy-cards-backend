from django.conf.urls import url
from authentication import views

urlpatterns = [
    url("login", views.login, name="login"),
    url("signup", views.sign_up, name="sign_up")
]

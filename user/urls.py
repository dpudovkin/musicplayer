
from django.urls import path

from . import views
from .views import SignUpView

app_name = "user"

urlpatterns = [
    path("info/", views.user_info, name="user_info"),
    path('signup/', SignUpView.as_view(), name='signup'),
]
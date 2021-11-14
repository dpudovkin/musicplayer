from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from user.forms import UserForm


@login_required(login_url='/accounts/login')
def user_info(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)

    user_form = UserForm(data=request.user)
    return render(request=request, template_name="user.html", context={'user_form': user_form})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
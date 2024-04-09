from django.shortcuts import render
from allauth.account.views import SignupView
from .forms import CustomSignupForm


# Create your views here.
class CustomSignupView(SignupView):
    form_class = CustomSignupForm

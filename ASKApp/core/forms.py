from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset = Skill.objects.all(), required=False)
    class Meta:
        model = Profile
        fields = ['bio', 'image', 'skills']
        
class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question_text', 'is_anonymous', 'skills']
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['answer_text']
        
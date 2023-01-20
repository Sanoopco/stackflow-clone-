from django import forms
from qsapp.models import MyUser
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from qsapp.models import Questions

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=MyUser
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "profile_pic",
            "password1",
            "password2"
            ]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "phone":forms.TextInput(attrs={"class":"form-control"}),
            
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-2"}))
    
class QuestionForm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=[
            "question",
            "images",
        ]
        widgets={
            "question":forms.Textarea(attrs={"class":"form-control mt-2","rows":3}),
            "images":forms.FileInput(attrs={"class":"form-select"})
        }
        
class AnswerForm(forms.Form):
    answer=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":6}))

class ChangePasswordForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2'}))
    
    class Meta:
        model = MyUser
        fields = [
            "old_password", 
            "new_password1", 
            "new_password2"
            ]

from django.shortcuts import redirect, render
from django.views.generic import TemplateView,CreateView,View,FormView,DetailView,ListView
from qsapp.forms import LoginForm, RegistrationForm,AnswerForm,ChangePasswordForm
from qsapp.models import MyUser,Questions,Answers
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from qsapp.forms import QuestionForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
# Create your views here.

#decorator
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"u must login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    model=Questions
    form_class=QuestionForm
    template_name="home.html"
    success_url=reverse_lazy("home")
    context_object_name="questions"  
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

class ChangePasswordView(auth_views.PasswordChangeView):
    model = MyUser
    form_class = ChangePasswordForm
    template_name="changepassword.html"
    success_url = reverse_lazy("home")
    


class SignUpView(CreateView):
    model=MyUser
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

class SignInView(FormView):
    form_class=LoginForm
    template_name="login.html"
    # def get(self, request, *args, **kwargs):
    #     form=LoginForm()
    #     return render(request,"login.html",{"form":form})
    def post(self, request, *args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=pwd)
            if user:
                login(request,user=user)
                messages.success(request,"login has been completed")
                return redirect("home")
            else:
                messages.error(request,"login has failed")
                return redirect("signin")



    
@method_decorator(decs,name="dispatch") 
class MyQuestionsView(ListView):
    model=Questions
    template_name='myquestions.html'
    context_object_name='myqs'
    def get_queryset(self):
        return Questions.objects.filter(user=self.request.user)

@method_decorator(decs,name="dispatch")
class QuestionDetailView(DetailView,FormView):
    model=Questions
    template_name="questiondetail.html"
    form_class=AnswerForm
    pk_url_kwarg="id"
    context_object_name="question"
    
decs
def add_answer(request, *args, **kwargs):
    if request.method=='POST':
        form=AnswerForm(request.POST)
        if form.is_valid():
            answer=form.cleaned_data.get("answer")
            qsid=kwargs.get("id")
            qs=Questions.objects.get(id=qsid)
            Answers.objects.create(user=request.user,answer=answer,question=qs)
            return redirect('home')
        else:
            return redirect('home')

#localhost/answers/id/remove/
decs
def remove_answer(request, *args,**kwargs):
    ans_id=kwargs.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.delete()
    return redirect('home')
decs
def up_vote(request,*args,**kwargs):
    ansid=kwargs.get("id")
    answer=Answers.objects.get(id=ansid)
    answer.up_vote.add(request.user)
    print(answer.up_vote.all())
    answer.save()
    return redirect('home')

def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect('signin')

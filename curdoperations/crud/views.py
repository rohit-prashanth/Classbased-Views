from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .forms import HomeForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
class Home(View):
    def get(self,request):
        form = HomeForm()
        return render(request,'home.html',{'fm':form})

    def post(self,request):
        form = HomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'You have successfully signed up!!')
            return HttpResponseRedirect('/')

class UserLogin(View):
    def get(self,request):
        form = AuthenticationForm()
        return render(request,'home.html',{'fm':form})
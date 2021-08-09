from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .forms import HomeForm, curdforms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from .models import CurdOperations


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
        form1 = AuthenticationForm()
        return render(request,'userlogin.html',{'fm':form1})

    def post(self,request):
        if not request.user.is_authenticated:
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                user = fm.cleaned_data['username']
                pwd = fm.cleaned_data['password']
                user = authenticate(username=user, password=pwd)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in Succesfully")
                    return HttpResponseRedirect("/userprofile/")

        else:
            return HttpResponseRedirect("/userprofile/")


class UserProfile(View):
    def get(self,request):
        if request.user.is_authenticated:
            fm = curdforms()
            data = CurdOperations.objects.all()
            return render(request, 'userprofile.html', {"name": request.user,'fm':fm, 'data':data})
        else:
            return HttpResponseRedirect("/login/")

    def post(self,request):
        fm = curdforms(request.POST)
        if fm.is_valid():
            name = fm.cleaned_data['name']
            email = fm.cleaned_data['email']
            request.session['name'] = name
            request.session['address'] = email
            request.session.set_expiry(600)
            fm.save()
            return HttpResponseRedirect('/userprofile/')

class DeleteRow(View):
    def post(self,request,id):
        row = CurdOperations.objects.get(pk=id)
        row.delete()
        return HttpResponseRedirect('/userprofile/')


class UpdateRow(View):
    def get(self,request,id):
        data = CurdOperations.objects.get(pk=id)
        form = curdforms(instance=data)
        return render(request, 'update.html', {'form': form})
    def post(self,request,id):
        data = CurdOperations.objects.get(pk=id)
        form = curdforms(request.POST, instance=data)
        form.save()
        messages.info(request, 'Updated Successfully')
        return HttpResponseRedirect('/userprofile/')


class UserLogout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/login/')
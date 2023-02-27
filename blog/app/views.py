from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib.auth import authenticate,login,logout
from .models import Post
# Create your views here.
from django.contrib import messages
def home(request):
    posts = Post.objects.all();
    return render(request,'app/home.html',{'posts':posts})
def about(request):
    return render(request,'app/about.html')
def contact(request):
    return render(request,'app/contact.html')
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request,'app/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
def user_signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"you are author")
            form.save()
        else:
            form = SignUpForm()
    return render(request,'app/signup.html',{'form':form})
def user_login(request):
    form = LoginForm()
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'logged in successfully')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request,'app/login.html',{'form':form})
    else:
        print("sdf");
        return HttpResponseRedirect('/dashboard/')
        
def add_post(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title,desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request,'app/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method =='POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'app/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
def delete_post(request,id):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/login/')
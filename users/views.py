from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ProfileModelForm
from .models import ProfileModel

def profile_view(request, id):
    try:
        profile = ProfileModel.objects.get(user=id)
    except ProfileModel.DoesNotExist:
        return redirect('home')
    return render(request, 'registration/profile.html', context={
        'profile' : profile,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')


def signup_view(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return redirect('login')
    else:
        form = UserForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



# def add_profile_view(request):
#     profile = ProfileModel.objects.get(user=request.user) 

#     if request.method == 'POST':
#         form = ProfileModelForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ProfileModelForm(instance=profile)
        
#     return render(request, 'registration/add-profile.html', context={'form': form})


from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignupForm

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return render(request, 'sign/sign_in.html')

def sign_up(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.created_user()
            login(request, user)
            return redirect('index')
    context = {
        'form':form,
    }
    return render(request, 'sign/sign_up.html', context)

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


from django.contrib.auth import login
from django.shortcuts import redirect, render

from ..forms import SignupModelForm

__all__ = (
    'sign_up',
)

def sign_up(request):
    form = SignupModelForm()
    if request.method == 'POST':
        form = SignupModelForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.created_user()
            user.save()
            login(request, user)
            return redirect('index')
    context = {
        'form':form,
    }
    return render(request, 'sign/sign_up.html', context)
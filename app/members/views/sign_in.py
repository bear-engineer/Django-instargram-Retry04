from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
__all__ = (
    'sign_in',
)

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            # next값이 전달되지 않았으면 post-list로 redirect
            return redirect('posts:post-list')
        else:
            return redirect('members:sign-in')
    return render(request, 'sign/sign_in.html')
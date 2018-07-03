from django.contrib.auth import logout
from django.shortcuts import redirect
__all__ = (
    'sign_out',
)

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

import json

import requests
from django.conf import settings
from django.contrib.auth import login, get_user_model, authenticate
from django.shortcuts import redirect

User = get_user_model()

__all__ = (
    'facebook_login',
)

def facebook_login(request):
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    if user is not None:
        # 생성한 유저로 로그인
        login(request, user)
        return redirect('index')
    return redirect('members:sign-in')
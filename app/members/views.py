import requests
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from config import settings
from .forms import SignupForm
User = get_user_model()

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

def sign_in_facebook(request):

    # 액세스 토큰 교환
    # GET parameter 의 'code'에 값이 전달됨 (authentication code)
    code = request.GET.get('code')
    url = 'https://graph.facebook.com/v3.0/oauth/access_token'
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri':'http://localhost:8000/members/facebook-login/',
        'client_secret':settings.FACEBOOK_APP_SECRET_CODE,
        'code':code
    }
    response = requests.get(url, params)
    response_dict = response.json()
    access_token = response_dict['access_token']

    # 액세스 토큰 검사
    debug_url = 'https://graph.facebook.com/debug_token'
    debug_params = {
        'input_token':access_token,
        'access_token':f'{settings.FACEBOOK_APP_ID}|{settings.FACEBOOK_APP_SECRET_CODE}',
    }
    debug_response = requests.get(debug_url, debug_params)

    # GraphAPI를 'me'(User)를 이용해서 Facebook User정보 받아오기
    url = 'https://graph.facebook.com/v3.0/me'
    params = {
        'fields':','.join([
           'id',
            'name',
            'first_name',
            'last_name',
            'picture',
        ]),
        'access_token': access_token
    }
    response = requests.get(url, params)
    response_dict = response.json()

    # 받어온 정보 중 회원가입에 필요한 요서 꺼내기
    facebook_user_id = response_dict['id']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_img_profile = response_dict['picture']['data']['url']

    user, user_created = User.objects.get_or_create(
        username=facebook_user_id,
        defaults={
            'first_name':first_name,
            'last_name':last_name,
            'profile_image':url_img_profile,
        }
    )

    login(request, user)
    return redirect('index')



def follow_toggle(request):
    if request.method == 'POST':
        request.user.username.follow()

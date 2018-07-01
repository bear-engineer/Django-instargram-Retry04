from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(max_length=50, label='ID')
    last_name = forms.CharField(max_length=50, label='Your name')
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput()
    )
    profile_image = forms.ImageField(
        label='프로필 이미지',
        required=False,
    )
    gender = forms.ChoiceField(
        label='성별',
        widget=forms.Select(),
        required=True,
        choices=User.CHOICE_GENDER,
    )
    site = forms.URLField(
        label='나의 홈페이지',
        widget=forms.URLInput(),
        required=False,
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            raise ValidationError('중복된 ID 입니다.')
        return username

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            self.add_error('password2', '비밀번호가 일치하지 않습니다.')
        else:
            return self.cleaned_data

    def created_user(self):
        username = self.cleaned_data['username']
        last_name = self.cleaned_data['last_name']
        password = self.cleaned_data['password2']
        profile_image = self.cleaned_data['profile_image']
        gender = self.cleaned_data['gender']
        site = self.cleaned_data['site']

        user = User.objects.create_user(
            username=username,
            last_name=last_name,
            password=password,
            profile_image=profile_image,
            gender=gender,
            site=site,
        )
        return user
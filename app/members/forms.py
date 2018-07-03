from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class SignupModelForm(forms.ModelForm):
    password2=forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields =['username', 'last_name', 'password','password2', 'profile_image', 'gender', 'site']
        widgets = {
            'password': forms.PasswordInput(),
        }


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
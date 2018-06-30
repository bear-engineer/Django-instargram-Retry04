from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_image = models.ImageField(blank=True, upload_to='profile')
    site = models.URLField(blank=True)
    email = models.EmailField()
    CHOICE_GENDER = (
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택하지 않습니다.')
    )
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER)
    created_at = models.DateTimeField(auto_now_add=True)


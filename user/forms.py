from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.db import models

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        error_messages={"required": "이메일을 입력해주세요."}, max_length=64, label="이메일"
    )
    username = forms.CharField(
        error_messages={"required": "유저이름을 입력해주세요."},
        label="유저명",
    )
    password1 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호",
    )
    password2 = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호 확인",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


## 로그인 폼 
class LoginForm(forms.ModelForm):
    """로그인 폼"""
    # TODO: 2. login 할 때 form을 활용해주세요
    class Meta:
        model = User
        fields = {"username", "password"}
        widgets = {
            "username": forms.TextInput(attrs={"style": "width:270px;"}),       # 사용자ID
            "password": forms.PasswordInput(attrs={"style": "width:270px;"}),   # 비밀번호
        }

    # 입력된 사용자ID에 대해서 등록된 회원인지 확인한다.
    def clean__Username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
            return username
        except models.User.DoesNotExist:
            self.add_error("username", forms.ValidationError("사용자ID를 잘못 입력했습니다."))

    # 사용자ID가 정상적으로 입력된 경우, 입력된 비밀번호를 확인한다.
    def clean(self):
        password = self.cleaned_data.get("password")    # 비밀번호
        username = self.cleaned_data.get("username")    # 사용자ID
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 일치하지 않습니다."))
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError("사용자ID를 잘못 입력했습니다."))

        return super().clean()
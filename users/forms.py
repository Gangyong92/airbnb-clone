from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    # widget=forms.PasswordInput 문자로 출력되지 않도록 옵션 추가
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        # 유저가 보낸 데이터에서 email을 찾음
        email = self.cleaned_data.get("email")
        try:
            # 그리고 username에서 email과 같은게 있는지 찾음
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            # 없으면 애러
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            # 그리고 username에서 email과 같은게 있는지 찾음
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is wrong")
        except models.User.DoesNotExist:
            pass
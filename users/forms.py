from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    # widget=forms.PasswordInput 문자로 출력되지 않도록 옵션 추가
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            # 그리고 username에서 email과 같은게 있는지 찾음
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                # 필드를 통합한 clean method를 썻다면 무조건 cleaned_data를 써야함
                return self.cleaned_data
            else:
                # clean method를 사용할 때는 raise말고 add_error
                # 로 애러가 뜨는 필드를 지정해줘야함.
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))
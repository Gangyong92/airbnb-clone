from django import forms
from django.contrib.auth.forms import UserCreationForm
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


# UserCreationForm안에 password_validation.validate_password가 중요함.
# 그대로 상속 받아 쓰거나 UserCreationForm안에 내용 긁어와서 Overriding
# 해서 사용하면 됨.
class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()

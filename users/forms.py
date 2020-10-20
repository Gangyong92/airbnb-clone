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


class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    # password1은 이름이 마음에 안드니까 label을 줌
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # validate 필요 필드, email, password, password1
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            # 사용중인 email 없을 때 반환함.
            return email

    # clean_password하면 1이 clean전 이라서 가지고 올 수 없음. 그래서 1 기준으로 만듬.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # password를 암호화 해야하기 때문에 create가 아닌 create_user를 사용
        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

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


# Model에 연결된 Form 활용 방법: ModelForm 사용
# 유니크 필드는 ModelForm에서 알아서 validate 처리해줘서 예외처리 안해줘도 됨.
# 안에 save method도 있음 object를 DB에 save 해줌
class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    # password는 user가 가지고 있지 않으니까 그대로 두자
    password = forms.CharField(widget=forms.PasswordInput)
    # password1은 이름이 마음에 안드니까 label을 줌
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # clean_password하면 1이 clean전 이라서 가지고 올 수 없음. 그래서 1 기준으로 만듬.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        # commit=False 옵션은 object는 생성하지만 db에는 올리지 말라는 뜻임
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        # password를 암호화 시켜줌
        user.set_password(password)
        user.save()

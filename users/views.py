from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "itn@las.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        # clean method에서 except가 떴으면 유효데이터가 아니라서 False가 뜰거임
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})
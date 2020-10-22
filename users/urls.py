from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    # key라는 이름으로 str형태로 가져올거임. 그리고 complete_verification에 key로 넘겨줌
    path("verify/<str:key>", views.complete_verification, name="complete-verification"),
]

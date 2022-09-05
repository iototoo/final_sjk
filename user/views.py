from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, RegisterForm

User = get_user_model()

##### 메인 

def index(request):
    return render(request, "index.html")


#### 사용자 등록하고 로그인 페이지로 이동
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

#### 
def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username") # 사용자ID
            password = request.POST.get("password") # 비밀번호
            user = authenticate(request, username=username, password=password)
            if user is None:
                return redirect(reverse("login"))
            login(request, user)
            return redirect(reverse("index"))
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


## 로그아웃
def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse("index"))
    else:
        return redirect(reverse("login"))


## 사용자 리스트
# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
# 프로젝트 환경설정(settings.py)에 LOGIN_URL 설정 필요
@login_required
def user_list_view(request):
    users = User.objects.all()
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "users.html", {"users": page_obj})


# ======================================================================================================================
# 페이징을 확인하기 위해 더미 사용자 생성
# 사용법: localhost:8000/dummy/dummy/
# - 무작위로 사용자를 100개 생성한다.
# ======================================================================================================================
def create_dummy_users_view(request):
    users = []
    for i in range(100):
        user = User(first_name='User%dFirstName' % i,
                    last_name='User%dLastName' % i,
                    username='user%d' % i,
                    email='user%d@mydomain.com' % i,
                    password='hashedPasswordStringPastedHereFromStep1!',
                    is_active=True,
                    )
        users.append(user)

    User.objects.bulk_create(users)

    return  render(request)


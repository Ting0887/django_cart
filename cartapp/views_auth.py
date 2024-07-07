from django.http.response import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render ,get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from cartapp import models,send_email_user
from .forms import RegisterForm,LoginForm,PwchangeForm,PasswordForgetForm
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import RegisterSerializer

def sign_up(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password1 = form.cleaned_data['password1']
            
            print(firstname, email, password1, phone)
            user = models.User.objects.create_user(username = firstname + ' ' + lastname,
                                                   first_name = firstname,
                                                   last_name = lastname,
                                                   password = password1,
                                                   email = email)
            
            models.UserProfile.objects.create(user=user,
                                              phone=phone)

            return HttpResponseRedirect('/login/')
    return render(request,"accounts/register.html",{'form':form})

def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
    
            user = models.User.objects.get(email=email)
            user = auth.authenticate(username=user.username, password=password)
            
            print(user)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect(f'/profile/{user.id}/')
            else:
                #login fail
                return render(request,"accounts/login.html",{'form':form,'error_message':'密碼不正確'})
    else:
        form = LoginForm()
    return render(request,"accounts/login.html",{'form':form})

@login_required(login_url='Login')
def user_logout(request):
    cart = request.session.get('cartlist',[])
    auth.logout(request)
    request.session['cartlist'] = cart
    return redirect('/login')    

@login_required(login_url='Login')
def change_password(request,pk):
    user = get_object_or_404(models.User, pk=pk)
    # 验证当前用户是否是待修改密码的用户
    if request.user != user:
        return HttpResponseForbidden("您沒有權限修改該使用者的密碼")
    
    if request.method == 'POST':
        form = PwchangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            if user.check_password(old_password):
                # 设置新密码
                new_password = form.cleaned_data['password1']
                user.set_password(new_password)
                user.save()
    else:
        form = PwchangeForm(user=request.user)

    return render(request, "accounts/pwd_change.html", {'form': form, 'user': user})

def forget_password(request):
    #input email and notify customer reset password
    form = PasswordForgetForm()
    if request.method == 'POST':
        form = PasswordForgetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = models.User.objects.filter(email=email)        
            #如果帳號存在
            print(associated_users)
            if associated_users.exists():
                success_message = '已經發送重設密碼資訊到您的信箱'
                print(success_message)
                for user in associated_users:
                    mailto = user.email
                    mailsubject = '動漫購物網 - 密碼重設通知'
                    mailcontent = f"""{user}您好,\n您的密碼需要重新設定,\n請點入此連結重設密碼 : http://127.0.0.1:8000/reset/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}"""                              
                    send_email_user.send_simple_message(mailto, mailsubject, mailcontent)
                    
                    return render(request, "accounts/forget_pwd.html",context={"form":form, "Message":success_message})
  
    return render(request, "accounts/forget_pwd.html",context={"form":form})

@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    print(user)
    _, token = AuthToken.objects.create(user)
    
    return Response({'user_info':
                            {'username':user.username,
                             'email':user.email},
                    'token':token
                    })

@api_view(['GET'])
def get_user_data(request):
    user = request.user
    print(user)
    if user.is_authenticated:
        return Response({'user_info':
                            {'username':user.username,
                             'email':user.email},
                        })
    
    return Response({'error':'not authenticated'},status=400)

@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.save()
    _,token = AuthToken.objects.create(user)
    return Response({'user_info':
                            {'id':user.id,
                             'username':user.username,
                             'email':user.email},
                    'token':token
                    })
    
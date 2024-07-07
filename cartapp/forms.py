from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

class RegisterForm(UserCreationForm):
    firstname = forms.CharField(
        label="FirstName",max_length=50,
        widget= forms.TextInput(attrs={'id':'firstname','placeholder':'FirstName'})
    )
    lastname = forms.CharField(
        label="LastName",max_length=50,
        widget= forms.TextInput(attrs={'id':'lastname','placeholder':'LastName'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget= forms.EmailInput(attrs={'id':'email','placeholder':'email'})
    )
    phone = forms.IntegerField(
        label="手機號碼",
        widget=forms.NumberInput(attrs={'id':'phone','placeholder':'phone'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget= forms.PasswordInput(attrs={'id':'password1','placeholder':'密碼'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget= forms.PasswordInput(attrs={'id':'password2','placeholder':'確認密碼'})
    )
    def clean_username(self):
        firstname = self.cleaned_data.get('firstname')
        if len(firstname) < 3:
            raise forms.ValidationError("帳號名稱不可小於3個字元")
        elif len(firstname) > 20:
            raise forms.ValidationError("帳號名稱太短")
        else:
            filter_result = User.objects.filter(username__exact=firstname)
            if len(filter_result) > 0:
                raise forms.ValidationError("帳號已經存在")
        return firstname
    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if len(lastname) < 3:
            raise forms.ValidationError("帳號名稱不可小於3個字元")
        elif len(lastname) > 20:
            raise forms.ValidationError("帳號名稱太短")
        else:
            filter_result = User.objects.filter(username__exact=lastname)
            if len(filter_result) > 0:
                raise forms.ValidationError("帳號已經存在")
        return lastname
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(email)
        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("信箱已經存在")

        return email
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

class LoginForm(forms.Form):
    email = forms.CharField(
        label="帳號",max_length = 50,
        widget= forms.TextInput(attrs={'id':'email','placeholder':'帳號'})
    )
    password = forms.CharField(
        label="密碼",
        widget= forms.PasswordInput(attrs={'id':'password','placeholder':'密碼'})
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        filter_result = User.objects.filter(email=email)
        if len(filter_result) == 0:
            raise forms.ValidationError("使用者帳號不存在")
        return email
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password == None:
            raise forms.ValidationError("請輸入密碼")
        return password
    
class PasswordForgetForm(forms.Form):
    email = forms.EmailField(
        label="電子郵件",max_length=256,
        widget  = forms.EmailInput(attrs={'id': 'email',
                                          "placeholder":"Email",
                                          "style":"width:250px ;height: 30px;"})
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("此電子郵件沒有註冊過。")
        return email
            

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
            label="New Password",
            widget=forms.PasswordInput
            )
    password2 = forms.CharField(
            label="Confirm Password",
            widget=forms.PasswordInput
    )
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("你的密碼太短")
        elif len(password1) > 20:
            raise forms.ValidationError("你的密碼太長")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("密碼不匹配")
        return password2
            
class ProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name",max_length=50,required=False,
                                 widget= forms.TextInput(attrs={'placeholder':'First Name',"style":"width: 15%", "id":"firstname"}))
    last_name = forms.CharField(label="Last Name",max_length=50,required=False,
                                widget= forms.TextInput(attrs={'placeholder':'Last Name',"style":"width: 15%", "id":"lastname"}))
    phone = forms.CharField(label="Phone",max_length=50,required=True,
                            widget= forms.TextInput(attrs={'placeholder':'Phone',"style":"width: 15%", "id":"phone"}))
    
class PwchangeForm(forms.Form):
    old_password = forms.CharField(label="舊密碼",widget=forms.PasswordInput)
    password1 = forms.CharField(label="新密碼",widget=forms.PasswordInput)
    password2 = forms.CharField(label="密碼確認",widget=forms.PasswordInput)
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("你的密碼太短")
        elif len(password1) > 20:
            raise forms.ValidationError("你的密碼太長")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("密碼不匹配")
        return password2
from django.shortcuts import redirect, render,HttpResponse,get_object_or_404
from cartapp import models
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='Login')
def profile(request,pk):
    user = get_object_or_404(models.User, pk=pk)
    return render(request,"users_profile/profile.html",{'user':user})

@login_required(login_url='Login')
def profile_update(request, pk):
    user = get_object_or_404(models.User, pk=pk)

    user_profile = get_object_or_404(models.UserProfile)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
              
            user_profile.phone = form.cleaned_data['phone']
            user_profile.save()
            
            user.username = user.first_name + ' ' + user.last_name
            user.save()
            print(user_profile)
            print('更新成功!')

            return redirect(f'/profile/{user.id}/')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user_profile.phone,
        }
        form = ProfileForm(initial=initial_data)
    
    return render(request, "users_profile/profile_update.html", {'form': form, 'user': user})
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, "You have successfully logged in!")
                return redirect('accounts:profile')
    else:
        form = AuthenticationForm()
    messages.error(request, "Couldn't log you in. Please try again.")
    return render(request, 'accounts/login.html', {'form': form})


def profile_view(request):
    return render(request, 'accounts/profile.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        # return render(request, 'accounts/logout.html')
        # return redirect('accounts/logout.html')
        return redirect('songs:song_list')

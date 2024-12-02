from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserForm
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver

@login_required
def login_root_redirect(request):
    """
    Redirect users based on their role (creator or taker).
    """
    try:
        # Retrieve the user's profile to check their role
        profile = Profile.objects.get(user=request.user)

        # Redirect based on the role
        if profile.role == 'creator':
            return redirect('home')  # Redirect creators to 'home'
        elif profile.role == 'taker':
            return redirect('results')  # Redirect takers to 'results'

        # Fallback in case role is missing or invalid
        return redirect('403')
    except Profile.DoesNotExist:
        # Handle the case where a Profile is not found for the user
        logout(request)
        return redirect('404')  # Redirect to the login page or a safe route
    

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the User object
            # Extract the role and save it in the Profile model
            # If the form is valid, the cleaned and validated data is stored in form.
            role = form.cleaned_data.get('role')
            Profile.objects.create(user=user, role=role)
            
            # Log the user in
            login(request, user)
            if role == 'creator':
                return redirect("home")
            elif role == 'taker':
                return redirect('results')
    else:
        form = UserForm()
    return render(request, 'easy_survey/register.html', {'form': form})
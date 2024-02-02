from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.contrib import messages
from .models import Details
from .forms import RegistrationForm, ProfileEditForm
from actions.models import Action


# login page view is to have login functionality, here credentials are hardcoded. we use this view for login page.
def login(request):
    return render(request, 'users/user/login.html')

def login_page(request):
        error_message = None
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        User = get_user_model()
        #user = authenticate(username = username, password = password)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None and (password == user.password):
            request.session['username'] = user.username
            request.session['access'] = user.details.role
            messages.add_message(request, messages.SUCCESS, "You have logged in succesfully")
            return redirect('tripobeatApp:alternate_page')
        else:
            messages.add_message(request, messages.ERROR, "Invalid Credentials, please try again")
        return render(request, 'users/user/login.html')

#logout is to logout for the user. It redirects to the home page after logout
def logout_page(request):
    if 'username' in request.session:
        del request.session['username']
    if 'access' in request.session:
        del request.session['access']
    return redirect('tripobeatApp:home_page')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    details, created = Details.objects.get_or_create(user=user)
    if request.session.get('access') == 'admin' or request.session.get('username') == user.username:
        if request.method == 'POST':
            form = ProfileEditForm(request.POST)
            if form.is_valid():
                # Update user data with the form data
                user.password = form.cleaned_data['password']
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                gender = form.cleaned_data['gender']
                user.save()

                if request.session.get('username') != user.username:
                    role = form.cleaned_data['role']
                    old_role = details.role
                    details.role = role
                details.gender = gender
                details.save()
                if request.session.get('username') != user.username:
                    if old_role != form.cleaned_data['role']:
                        action = Action(
                            user=user,
                            verb=" role has been changed from " + old_role + " to " + form.cleaned_data['role'],
                            role_changed=True,
                        )
                        action.save()
                messages.success(request, 'Profile updated successfully.')
        else:
            form = ProfileEditForm(initial={
                'password': user.password,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.details.gender if hasattr(user, 'details') else None,
                'role': user.details.role if hasattr(user, 'details') else 'regular',
            })
    else:
        actions = Action.objects.filter(user_id=user.id).order_by('-created')
        return render(request, 'users/user/profile.html', {"user": user, "actions": actions})
    actions = Action.objects.filter(user_id=user.id).order_by('-created')
    return render(request, 'users/user/profile.html', {"user": user, 'form': form, 'actions': actions})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']

            user = User.objects.create(username=username, email=email, password=password, first_name=first_name,
                                       last_name=last_name)
            details, created = Details.objects.get_or_create(user=user)
            details.gender = gender
            details.save()

            request.session['username'] = user.username
            messages.success(request, f"{user.username} registered successfully")
            return redirect("tripobeatApp:alternate_page")
    else:
        form = RegistrationForm()
    return render(request, 'users/user/register.html', {'form': form})

def user_profiles(request):
    user_names = User.objects.values_list('username', flat=True)
    return render(request, 'users/user/other_profiles.html', {'user_names': user_names})

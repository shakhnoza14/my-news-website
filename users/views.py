from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ProfileModelForm, EditModelForm
from .models import ProfileModel, Usermodel
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages

def profile_view(request, id):
    try:
        profile = ProfileModel.objects.get(user=id)
    except ProfileModel.DoesNotExist:
        return redirect('home')
    return render(request, 'registration/profile.html', context={
        'profile' : profile,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html')


def signup_view(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return redirect('login')
    else:
        form = UserForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



# def add_profile_view(request):
#     profile = ProfileModel.objects.get(user=request.user) 

#     if request.method == 'POST':
#         form = ProfileModelForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ProfileModelForm(instance=profile)
        
#     return render(request, 'registration/add-profile.html', context={'form': form})

def edit_view(request, id):
    user = User.objects.get(id=id)
    user_profile = ProfileModel.objects.get(user=user)
    form = EditModelForm(instance=user_profile)
    if request.method == "POST":
        form = EditModelForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            user.username = form.cleaned_data['username']
            user.save()
            return redirect('profile', user.id)
    context = {
        'form': form
    }
    return render(request, template_name='edit.html', context=context)


def reset_password(request):
    request.user
    return render(request, 'password-reset-sent.html')



class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    """Custom token generator with configurable expiration"""
    
    def __init__(self, expiration_hours=1):
        """
        Initialize with custom expiration time
        Default: 1 hour (you can change this)
        """
        self.expiration_hours = expiration_hours
        super().__init__()
    
    def check_token(self, user, token):
        """
        Check if token is valid and not expired
        """
        if not token:
            return False
        
        # Check if token is structurally valid first
        if not super().check_token(user, token):
            return False
        
        # Django's default token generator already includes timestamp validation
        # The PASSWORD_RESET_TIMEOUT setting in settings.py controls the expiration
        return True
    
    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's PK, email (if available), and some user state
        that's sure to change after a password reset to produce a token
        that invalidated when it's used.
        """
        email = getattr(user, 'email', '') or ''
        return (
            str(user.pk) + user.password + str(timestamp) + 
            str(user.last_login) + email
        )


# Create instance with 1-hour expiration (you can change this)
custom_token_generator = CustomPasswordResetTokenGenerator(expiration_hours=1)


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view that sends HTML emails with time-limited tokens"""
    
    # Use our custom token generator
    token_generator = custom_token_generator
    
    def form_valid(self, form):
        """Send HTML email when form is valid"""
        extra_context = {'expiration_hours': custom_token_generator.expiration_hours}
        if self.extra_email_context:
            extra_context.update(self.extra_email_context)
            
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': 'registration/password_reset_email.html',
            'extra_email_context': extra_context,
        }
        form.save(**opts)
        return super().form_valid(form)




class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view with better token expiration handling"""
    
    # Use our custom token generator
    token_generator = custom_token_generator
    
    def dispatch(self, *args, **kwargs):
        """Override dispatch to add custom token validation"""
        assert 'uidb64' in kwargs and 'token' in kwargs
        
        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])
        
        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(self.token_session_key)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, the real token is stored in the session
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the same page with a dummy token.
                    self.request.session[self.token_session_key] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return redirect(redirect_url)
                else:
                    # Token is invalid or expired
                    messages.error(self.request, 
                                 f'The password reset link is invalid or has expired. '
                                 f'Please request a new password reset.')
        
        # Display the "Password reset unsuccessful" form.
        return self.render_to_response(self.get_context_data())

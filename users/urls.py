from django.urls import path
from .views import signup_view, login_view, logout_view, profile_view, edit_view, CustomPasswordResetConfirmView, CustomPasswordResetView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,\
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:id>', profile_view, name='profile'),
    # path('add-profile/', add_profile_view, name='add_profile'),
    path('edit/<int:id>/', edit_view, name='edit'),
    # change password
    path('password_change/', PasswordChangeView.as_view(), name='password-change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
     
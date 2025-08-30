from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
   	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('refresh/', TokenRefreshView.as_view(), name='refresh'),
	path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
	path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
   
]

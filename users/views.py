from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import generate_reset_token, validate_reset_token, invalidate_reset_token
from django.core.mail import send_mail

User = get_user_model()

class RegisterView(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		data = request.data
		email = data.get('email')
		password = data.get('password')
		full_name = data.get('full_name')
		if not email or not password or not full_name:
			return Response({'error': 'All fields required.'}, status=status.HTTP_400_BAD_REQUEST)
		if User.objects.filter(email=email).exists():
			return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
		user = User.objects.create_user(email=email, password=password, full_name=full_name)
		return Response({'message': 'User registered.'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
	throttle_classes = [AnonRateThrottle]
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		email = request.data.get('email')
		password = request.data.get('password')
		user = authenticate(request, email=email, password=password)
		if user is not None:
			refresh = RefreshToken.for_user(user)
			return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)
		return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshView(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		refresh = request.data.get('refresh')
		try:
			token = RefreshToken(refresh)
			return Response({'access': str(token.access_token)}, status=status.HTTP_200_OK)
		except Exception:
			return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
	throttle_classes = [AnonRateThrottle]
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		email = request.data.get('email')
		user = User.objects.filter(email=email).first()
		if not user:
			return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
		token = generate_reset_token(user.id)
		# In production, send email. Here, just return token for demo.
		# send_mail('Password Reset', f'Your token: {token}', 'noreply@example.com', [email])
		return Response({'message': 'Reset token generated.', 'token': token}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		token = request.data.get('token')
		password = request.data.get('password')
		user_id = validate_reset_token(token)
		if not user_id:
			return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
		user = User.objects.filter(id=user_id).first()
		if not user:
			return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
		user.set_password(password)
		user.save()
		invalidate_reset_token(token)
		return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)


from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .tokens import generate_reset_token

User = get_user_model()

class AuthTests(APITestCase):
	def setUp(self):
		self.register_url = reverse('register')
		self.login_url = reverse('login')
		self.refresh_url = reverse('refresh')
		self.forgot_url = reverse('forgot-password')
		self.reset_url = reverse('reset-password')
		self.user_data = {
			'email': 'test@example.com',
			'password': 'TestPass123',
			'full_name': 'Test User'
		}
		self.user = User.objects.create_user(**self.user_data)

	def test_registration_success(self):
		data = {
			'email': 'new@example.com',
			'password': 'NewPass123',
			'full_name': 'New User'
		}
		response = self.client.post(self.register_url, data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(User.objects.filter(email=data['email']).exists())

	def test_registration_missing_fields(self):
		data = {'email': '', 'password': '', 'full_name': ''}
		response = self.client.post(self.register_url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_registration_duplicate_email(self):
		response = self.client.post(self.register_url, self.user_data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_login_success(self):
		response = self.client.post(self.login_url, {
			'email': self.user_data['email'],
			'password': self.user_data['password']
		})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)
		self.assertIn('refresh', response.data)
		self.access_token = response.data['access']
		self.refresh_token = response.data['refresh']

	def test_login_wrong_password(self):
		response = self.client.post(self.login_url, {
			'email': self.user_data['email'],
			'password': 'WrongPass'
		})
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_login_unregistered_email(self):
		response = self.client.post(self.login_url, {
			'email': 'unknown@example.com',
			'password': 'TestPass123'
		})
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_token_refresh_success(self):
		login_response = self.client.post(self.login_url, {
			'email': self.user_data['email'],
			'password': self.user_data['password']
		})
		refresh_token = login_response.data['refresh']
		response = self.client.post(self.refresh_url, {'refresh': refresh_token})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('access', response.data)

	def test_token_refresh_invalid(self):
		response = self.client.post(self.refresh_url, {'refresh': 'invalidtoken'})
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_forgot_password_success(self):
		response = self.client.post(self.forgot_url, {'email': self.user_data['email']})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('message', response.data)

	def test_forgot_password_unregistered_email(self):
		response = self.client.post(self.forgot_url, {'email': 'unknown@example.com'})
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_reset_password_success(self):
		token = generate_reset_token(self.user.id)
		response = self.client.post(self.reset_url, {'token': token, 'password': 'NewPass123'})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('NewPass123'))

	def test_reset_password_invalid_token(self):
		response = self.client.post(self.reset_url, {'token': 'invalidtoken', 'password': 'NewPass123'})
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

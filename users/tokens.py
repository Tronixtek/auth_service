import redis
import os
import uuid
from django.conf import settings

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.StrictRedis.from_url(REDIS_URL)

def generate_reset_token(user_id):
	token = str(uuid.uuid4())
	redis_client.setex(f"reset:{token}", 600, user_id)  # 10 min expiry
	return token

def validate_reset_token(token):
	user_id = redis_client.get(f"reset:{token}")
	if user_id:
		return user_id.decode()
	return None

def invalidate_reset_token(token):
	redis_client.delete(f"reset:{token}")

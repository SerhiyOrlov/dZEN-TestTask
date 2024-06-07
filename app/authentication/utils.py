import jwt

from django.conf import settings
from datetime import datetime, timedelta

from rest_framework import exceptions
MINUTES_IN_DAY = 1440


class JWTManager:
	"""
	Manager to work with jwt tokens

	generate_token(self, user_id, token_type):
	Generates a JWT token for a given user ID and token type.

	refresh_token(self, old_token):
		Refreshes a JWT token using the provided old token.

	_generate_jwt_token(payload):
		Generates a JWT token using the given payload.

	_extract_user_id_from_token(token):
		Extracts the user ID from the given token.

	decode_jwt_token(token):
		Decodes a JWT token and returns the payload.
	"""

	def generate_token(self, user_id, token_type):
		"""
		Generates a JWT token for a given user ID and token type.

		Parameters:
			user_id (int): The ID of the user for whom the token is being generated. Must be an integer.
			token_type (str): The type of token to generate. Must be either 'access' or 'refresh'.

		Returns:
			str: The generated JWT token.

		Raises:
			ValueError: If the user_id is not an integer or if the token_type is invalid.
		"""

		# Input data validation
		if not isinstance(user_id, int):
			raise exceptions.ValidationError({'user_id': 'User ID must be an integer'})

		print(f'Generating token for user_id: {user_id}')
		match token_type:
			case 'access':
				token_lifetime = 15
			case 'refresh':
				token_lifetime = MINUTES_IN_DAY
			case _:
				raise exceptions.ValidationError({'token': 'Invalid token type'})

		payload = {
			'user_id': user_id,
			'exp': datetime.utcnow() + timedelta(minutes=token_lifetime),  # Access token expiration time
			'iat': datetime.utcnow()
		}

		return self._generate_jwt_token(payload=payload)

	def refresh_token(self, old_token):
		"""
		Refreshes a JWT token using the provided old token.

		Parameters:
			old_token (str): The old JWT token to be refreshed.'.

		Returns:
			str: The new refreshed JWT token.

		Raises:
			ValueError: If the old_token format is invalid.
		"""
		# Input data validation
		if not isinstance(old_token, str):
			raise exceptions.ValidationError({'token': f'Token must be str, not {type(old_token)}'})

		user_id = self._extract_user_id_from_token(old_token)
		return self.generate_token(user_id, token_type='refresh')

	def _generate_jwt_token(self, payload):
		"""
		Generates a JWT token using the given payload.

		Parameters:
			payload (dict): The payload to include in the JWT token.

		Returns:
			str: The generated JWT token.
		"""
		return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

	def _extract_user_id_from_token(self, token):
		try:
			payload = self._decode_jwt_token(token)
			user_id = payload['user_id']
		except (IndexError, ValueError):
			raise exceptions.ValidationError({"token":  "Invalid token format"})
		return user_id

	def _decode_jwt_token(self, token):
		"""
		Decodes a JWT token and returns the payload.

		Parameters:
			token (str): The JWT token to decode.

		Returns:
			dict: The decoded payload, or None if the token is invalid or expired.

		Raises:
			jwt.ExpiredSignatureError: If the token has expired.
			jwt.InvalidTokenError: If the token is invalid.
		"""
		try:
			payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
		except jwt.ExpiredSignatureError:
			raise exceptions.ValidationError({'token': 'Refresh token has expired'})
		except jwt.InvalidTokenError:
			raise exceptions.ValidationError({'token': 'Invalid refresh token'})
		return payload


jwt_manager = JWTManager()

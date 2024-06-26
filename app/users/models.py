from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin  # PermissionMixin allows to add pemissions at the User model
)

from django.db import models

from authentication.utils import jwt_manager


class UserManager(BaseUserManager):
	"""
	UserManager is a required class for User model.
	Needed for managing User objects.
	"""

	def create_user(self, username, email, password=None):
		"""Creating a usual user without additonal permissions."""
		if username is None:
			raise TypeError('Users must have a username.')

		if email is None:
			raise TypeError('Users must have an email address.')

		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)  # A default Django method to set normalized and hashed password to the user
		user.save()

		return user

	def create_superuser(self, username, email, password):
		"""Create superuser who has permission to the admin panel"""
		if password is None:
			raise TypeError('Superusers must have a password.')

		user = self.create_user(username, email, password)
		user.is_superuser = True  # User has all permissions of applications
		user.is_staff = True  # User has permission to the admin panel, and superuser can set some restrictions
		user.save()

		return user


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(db_index=True, max_length=255, unique=True)
	email = models.EmailField(db_index=True, unique=True)
	_homepage = models.CharField(unique=True, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	_refresh_token = models.CharField(max_length=255, db_column='refresh_token', blank=True, null=True)
	USERNAME_FIELD = 'email'  # Email instead username in user authentications
	REQUIRED_FIELDS = ('username',)

	objects = UserManager()

	def __str__(self):
		"""Email as preview of the model in admin panel"""
		return self.email

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	@property
	def access_token(self):
		"""Function with property decorator allows to add an edditional atribute to the class"""
		return jwt_manager.generate_token(user_id=self.pk, token_type='access')

	@property
	def refresh_token(self):
		return self._refresh_token

	@refresh_token.setter
	def refresh_token(self, value):
		refresh_token = jwt_manager.generate_token(user_id=self.pk, token_type='refresh')
		self._refresh_token = refresh_token
		self.save(update_fields=['_refresh_token'])

	@property
	def hompage(self):
		return self._homepage

	@hompage.setter
	def hompage(self, value):
		homepage = self._generate_hompage()
		self._homepage = homepage
		self.save(update_fields=['_refresh_token'])

	def _generate_hompage(self):
		return f"profile/{self.username}"

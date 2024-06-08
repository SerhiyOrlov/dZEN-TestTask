from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
	"""
	Custom permission to only allow owners of an object or admin users to access it.
	"""
	def has_object_permission(self, request, view, obj):
		# Admins have access to the all objects
		if request.user.is_staff:
			return True

		# Owners have access to their objects.
		return obj == request.user

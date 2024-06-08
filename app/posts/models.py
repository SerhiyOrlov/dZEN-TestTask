from django.db import models


class Post(models.Model):
	author = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Post by {self.author} at {self.created_at}'

class Comment(models.Model):
	text = models.TextField()
	post = models.ForeignKey('Post', on_delete=models.CASCADE)
	author = models.ForeignKey('users.User', on_delete=models.CASCADE)
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Comment by {self.author} on {self.post} at {self.created_at}'

# Create your models here.

from django.db import models
# Models is where database is made
# Create your models here.
class User(models.Model):
	user_name = models.CharField(max_length = 255)
	email = models.EmailField(unique = True)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return "User: {}".format(self.user_name)

class Post(models.Model):
	content = models.CharField(max_length=255)
	author = models.ForeignKey(User, related_name="created_posts")
	# likers = models.ManyToManyField(User, related_name="liked_posts")
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

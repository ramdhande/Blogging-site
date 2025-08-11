from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
	title= models.CharField(max_length=100)
	content =models.TextField()
	date_posted =models.DateTimeField(default=timezone.now)
	image = models.ImageField(upload_to='post_images/', blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		url = reverse('post-detail', kwargs={'pk': self.pk})
		print(f"Generated URL: {url}")
		return url
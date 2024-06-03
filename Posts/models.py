from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_description = models.TextField()
    post_shortname = models.SlugField(max_length=100, unique=True)
    post_published_datetime = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    post_image = models.ImageField(upload_to='post/images/')


    def __str__(self):
        return self.post_title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_published_datetime = (models.DateTimeField
                                  (auto_now_add=True))

    def __str__(self):
        return self.comment_text
from django.db import models
import datetime
from users.models import User


class ModelTimeStamped(models.Model):
    modified_on = models.DateTimeField(auto_now=datetime.datetime.utcnow(), editable=False)
    created_on = models.DateTimeField(auto_now_add=datetime.datetime.utcnow(), editable=False)


class Blogs(ModelTimeStamped):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author_id = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    object = models.Manager()

    def __str__(self):
        return self.title


class Comment(ModelTimeStamped):
    content = models.TextField()
    blog_id = models.ForeignKey(Blogs, related_name='blog', on_delete=models.CASCADE)
    comment_author_id = models.ForeignKey(User, related_name='comment_author', on_delete=models.CASCADE)

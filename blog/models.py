from django.db import models
from django.utils import timezone


class PostManager(models.Manager):
    def recent_posts(self, how_many=3):
        return self.order_by('-published_date')[:how_many]


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    objects = PostManager()

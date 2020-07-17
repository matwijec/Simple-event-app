from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Participants(models.Model):
    participants = models.ManyToManyField(User)
    '''
    def save(self, *args, **kwargs):
        if not self.id:
            super(Participants, self).save(*args, **kwargs)
        # process self.parent_subject (should be called ...subjects, semantically)
        super(Participants, self).save(*args, **kwargs)
    '''

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ForeignKey(Participants, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
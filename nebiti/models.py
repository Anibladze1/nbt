from django.db.models import Sum
from django.contrib.auth.models import User
from django.db import models


class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    delegate = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    votes = models.ManyToManyField(Voter, through='Vote')

    class Meta:
        ordering = ['-id']

    def likes(self):
        likes_count = self.vote_set.filter(vote=True).count()
        return likes_count

    def dislikes(self):
        dislikes_count = self.vote_set.filter(vote=False).count()
        return dislikes_count


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.voter.name} voted {self.vote} on {self.post.title}'

    def cast_vote(self, voter, post, vote):
        delegate = voter.delegate
        if delegate:
            self.voter = delegate
        else:
            self.voter = voter
        self.post = post
        self.vote = vote
        self.save()


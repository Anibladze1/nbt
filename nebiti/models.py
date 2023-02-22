from django.db.models import Sum
from django.contrib.auth.models import User
from django.db import models


class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    delegate = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='delegated_by')
    delegated_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='delegate_of')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # If the voter already exists, check if they previously had a delegate
            old_voter = Voter.objects.get(pk=self.pk)
            if old_voter.delegated_to != self.delegated_to:
                # If the delegated_to attribute has changed, remove the old voter from the delegate list
                if old_voter.delegated_to is not None:
                    old_voter.delegated_to.delegate.remove(old_voter)

                # Add the current voter to the delegate list of their new delegate
                if self.delegated_to is not None:
                    self.delegated_to.delegate.add(self)

        super(Voter, self).save(*args, **kwargs)


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

    def __str__(self):
        return self.title


class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote = models.BooleanField(default=0)
    delegate = models.BooleanField(default=False)

    def cast_vote(self, voter, post, vote):
        delegate = voter.delegate
        if delegate:
            self.voter = delegate
            self.delegate = True
        else:
            self.voter = voter
        self.post = post
        self.vote = vote
        self.save()

    def __str__(self):
        return f'{self.voter.name} voted {self.vote} on {self.post.title}'

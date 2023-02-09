from django.contrib import admin
from . models import Post, Voter, Vote


# Register your models here.
admin.site.register(Post)
admin.site.register(Voter)
admin.site.register(Vote)


from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Branch(models.Model):
    name = models.CharField(max_length=30, unique=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)    
    branch = models.ForeignKey(Branch, related_name='branches', on_delete=models.PROTECT)
    


class Pr(models.Model):
    pr = models.IntegerField()
    status = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, related_name='prs', on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, related_name='prs', on_delete=models.PROTECT)
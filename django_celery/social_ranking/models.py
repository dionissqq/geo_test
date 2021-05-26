from django.db import models

# Create your models here.
class Rank(models.Model):
    user_id = models.IntegerField()
    score = models.IntegerField(default=0)
    
class RankChange(models.Model):
    user_id = models.IntegerField()
    d_score = models.IntegerField(default=0)
    information = models.CharField(max_length=128)
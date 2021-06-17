from django.db import models

class Score(models.Model):
    name=models.CharField(max_length=255)
    score=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
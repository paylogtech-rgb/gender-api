import uuid
from django.db import models

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100, unique=True)
    
    gender = models.CharField(max_length=10)
    gender_probability = models.FloatField()
    sample_size = models.IntegerField()
    
    age = models.IntegerField()
    age_group = models.CharField(max_length=20)
    
    country_id = models.CharField(max_length=10)
    country_probability = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.

from simnursebe.models import BaseModel
from main_utils.firestore import Firestore
from django.db import models

# Create your models here.


class Disease(models.Model):
    kr = models.TextField(blank=False)
    en = models.TextField(blank=False)

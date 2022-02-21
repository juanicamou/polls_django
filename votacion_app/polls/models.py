from pyexpat import model
from statistics import mode
from time import timezone
from django.db import models
import datetime

from django.forms import DateTimeField
from django.utils import timezone

class Question(models.Model):

    # id No es necesario, lo crea django solo
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        # datetime.timedelta(days=1) es igual a 1 día.


class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # on_delete=models.CASCADE -> Si elemino una pregunta, elimina las resp asociadas a esa pregunta.
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

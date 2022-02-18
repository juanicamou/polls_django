from pyexpat import model
from statistics import mode
from django.db import models
from django.forms import DateTimeField

class Question(models.Model):
    # id No es necesario, lo crea django solo
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # on_delete=models.CASCADE -> Si elemino una pregunta, elimina las resp asociadas a esa pregunta.
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

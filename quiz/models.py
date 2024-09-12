# quiz/models.py
from django.db import models

class Question(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    option_e = models.CharField(max_length=255, blank=True, null=True)
    correct_option = models.CharField(max_length=1)  # Assume valores 'A', 'B', 'C', 'D' ou 'E'

    def __str__(self):
        return self.question_text

# quiz/forms.py

from django import forms
from .models import Question

class QuizForm(forms.Form):
    answer = forms.ChoiceField(choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E')
    ], widget=forms.RadioSelect)

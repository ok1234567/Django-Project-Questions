# quiz/urls.py
from django.urls import path
from .views import start_quiz, question_view, results_view

urlpatterns = [
    path('', start_quiz, name='start_quiz'),
    path('question/<int:question_number>/', question_view, name='question'),
    path('results/', results_view, name='results'),
]

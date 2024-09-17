# quiz/urls.py
from django.urls import path
from .views import start_quiz, quiz_question, submit_quiz

urlpatterns = [
   path('', start_quiz, name='start_quiz'),
    path('question/<int:question_number>/', quiz_question, name='quiz_question'),
    path('submit/', submit_quiz, name='submit_quiz'),
]

# quiz/urls.py
from django.urls import path
from .views import start_quiz, question_view, results_view, question_list, question_add, question_edit, question_delete

urlpatterns = [
    path('', start_quiz, name='start_quiz'),
    path('question/<int:question_number>/', question_view, name='question'),
    path('results/', results_view, name='results'),
    path('admin/questions/', question_list, name='admin_question_list'),
    path('admin/questions/add/', question_add, name='admin_question_add'),
    path('admin/questions/edit/<int:pk>/', question_edit, name='admin_question_edit'),
    path('admin/questions/delete/<int:pk>/', question_delete, name='admin_question_delete'),
]

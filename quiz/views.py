# quiz/views.py
from django.shortcuts import render, redirect
from .models import Question
import random

def start_quiz(request):
    return render(request, 'quiz/start_quiz.html')

def question_view(request, question_number):
    questions = request.session.get('questions')

    if not questions:
        # Seleciona 20 perguntas aleatórias
        all_questions = list(Question.objects.all())
        random.shuffle(all_questions)
        questions = all_questions[:20]
        request.session['questions'] = [question.id for question in questions]
        request.session['answers'] = [None] * 20  # Para armazenar as respostas

    if question_number > 20:
        return redirect('results')

    question = Question.objects.get(id=request.session['questions'][question_number-1])

    if request.method == 'POST':
        selected_option = request.POST.get('option')
        if selected_option:
            answers = request.session['answers']
            answers[question_number-1] = selected_option
            request.session['answers'] = answers

        # Vai para a próxima pergunta
        if question_number < 20:
            return redirect('question', question_number + 1)
        else:
            return redirect('results')

    return render(request, 'quiz/question.html', {'question': question, 'question_number': question_number})

def results_view(request):
    questions = [Question.objects.get(id=qid) for qid in request.session.get('questions', [])]
    answers = request.session.get('answers', [])

    incorrect_questions = []
    score = 0
    for question, answer in zip(questions, answers):
        if question.correct_option == answer:
            score += 1
        else:
            incorrect_questions.append((question, answer, question.correct_option))

    return render(request, 'quiz/results.html', {
        'score': score,
        'incorrect_questions': incorrect_questions,
        'total': len(questions)
    })

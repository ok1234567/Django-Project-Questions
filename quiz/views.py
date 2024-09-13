# quiz/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question
from .forms import QuestionForm
import random

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'quiz/admin/question_list.html', {'questions': questions})

def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_question_list')
    else:
        form = QuestionForm()
    return render(request, 'quiz/admin/question_form.html', {'form': form, 'action': 'Add'})

def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('admin_question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'quiz/admin/question_form.html', {'form': form, 'action': 'Edit'})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('admin_question_list')
    return render(request, 'quiz/admin/question_confirm_delete.html', {'question': question})

def start_quiz(request):
    # Seleciona 20 perguntas aleatórias do banco de dados
    questions = list(Question.objects.all())
    random.shuffle(questions)
    selected_questions = questions[:20]

    # Armazena os IDs das perguntas selecionadas na sessão
    request.session['questions'] = [question.id for question in selected_questions]
    request.session['answers'] = [None] * 20  # Resetar respostas do usuário

    return render(request, 'quiz/start_quiz.html')

def question_view(request, question_number):
    questions_ids = request.session.get('questions')
    
    if not questions_ids or question_number > len(questions_ids):
        return redirect('results')

    question = Question.objects.get(id=questions_ids[question_number - 1])

    if request.method == 'POST':
        selected_option = request.POST.get('option')
        if selected_option:
            answers = request.session['answers']
            answers[question_number - 1] = selected_option
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

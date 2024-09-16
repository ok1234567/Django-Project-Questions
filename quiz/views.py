# quiz/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question
from .forms import QuestionForm
import random

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'admin/question_list.html', {'questions': questions})

def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_question_list')
    else:
        form = QuestionForm()
    return render(request, 'admin/question_form.html', {'form': form, 'action': 'Add'})

def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('admin_question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'admin/question_form.html', {'form': form, 'action': 'Edit'})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('admin_question_list')
    return render(request, 'admin/question_confirm_delete.html', {'question': question})

def start_quiz(request):
    # Seleciona 20 perguntas aleatórias do banco de dados
    questions = list(Question.objects.all())
    random.shuffle(questions)
    selected_questions = questions[:20]

    # Armazena os IDs das perguntas selecionadas na sessão
    request.session['questions'] = [question.id for question in selected_questions]
    request.session['answers'] = [None] * 20  # Resetar respostas do usuário

    return redirect('question', question_number=1)

def question_view(request, question_number):
    questions_ids = request.session.get('questions')
    question = Question.objects.get(pk=questions_ids[question_number - 1])

    return render(request, 'quiz/quiz_question.html', {
        'current_question_number': question_number,
        'current_question': question,
        'total_questions': len(questions_ids),
    })

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

def submit_quiz(request):
    questions = Question.objects.all()[:20]  # Pegue as primeiras 20 perguntas
    unanswered_questions = []
    correct_count = 0
    total_answered = 0  # Número de perguntas respondidas

    for i, question in enumerate(questions):
        selected_option = request.POST.get(f'question_{i + 1}')  # Obtenha a resposta selecionada
        if not selected_option:
            unanswered_questions.append(i + 1)  # Colete o número da pergunta não respondida
            continue  # Pule para a próxima pergunta, se não for respondida

        total_answered += 1  # Incrementa o número de perguntas respondidas
        if selected_option == question.correct_option:
            correct_count += 1  # Incrementa o contador de respostas corretas

    # Cálculo do resultado
    total_incorrect = total_answered - correct_count  # Apenas questões respondidas contam como erradas
    result = (correct_count * 5) + (total_incorrect * -2)  # Fórmula ajustada

    wrong_answers = []

    for i, question in enumerate(questions):
        selected_option = request.POST.get(f'question_{i + 1}')
        if selected_option and selected_option != question.correct_option:
            wrong_answers.append(question.id)

    # Passar a lista de respostas erradas para o template
    return render(request, 'quiz/results.html', {
        'correct_count': correct_count,
        'total_questions': len(questions),
        'total_answered': total_answered,
        'result': result,
        'wrong_answers': wrong_answers,
        'questions': questions,
    })


from django.shortcuts import render, redirect
from .models import Question
from django.http import HttpResponseRedirect
import random
import json

def start_quiz(request):
    # Selecionar 20 perguntas aleatórias
    questions = list(Question.objects.all())
    random.shuffle(questions)
    selected_questions = questions[:20]
    
    # Armazenar as perguntas na sessão
    request.session['questions'] = [question.id for question in selected_questions]
    request.session['answers'] = {}  # Respostas vazias no início
    
    return render(request, 'quiz/quiz_start.html')

def quiz_question(request, question_number):
    # Recupera todas as perguntas do quiz armazenadas na sessão
    question_ids = request.session.get('questions', [])
    questions = Question.objects.filter(id__in=question_ids)
    question = questions[question_number - 1]  # Pega a pergunta com base no número atual

    # Armazena a resposta enviada (caso o formulário tenha sido submetido)
    if request.method == 'POST':
        selected_answer = request.POST.get(f'answer_{question.id}')
        next_question = request.POST.get('next_question')  # Verifica se há navegação

        # Salva a resposta na sessão
        if selected_answer:
            if 'answers' not in request.session:
                request.session['answers'] = {}
            request.session['answers'][str(question.id)] = selected_answer
            request.session.modified = True

        # Se o usuário está navegando para outra pergunta
        if next_question:
            return redirect('quiz_question', question_number=next_question)
        
        # Se não houver navegação, redirecionar para a próxima pergunta
        if question_number < len(questions):
            return redirect('quiz_question', question_number=question_number + 1)

    # Carrega a resposta já dada (se existir) para a pergunta atual
    current_answer = request.session.get('answers', {}).get(str(question.id))

    return render(request, 'quiz/quiz_question.html', {
        'question': question,
        'question_number': question_number,
        'total_questions': len(questions),
        'current_answer': current_answer,  # Passa a resposta atual (se houver)
        'questionsIds' : [questionX.id for questionX in questions]
    })

def submit_quiz(request):
    questions = Question.objects.filter(id__in=request.session.get('questions', []))
    answers = request.session.get('answers', {})

    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    results = []

    for question in questions:
        selected_answer = answers.get(str(question.id))

        if not selected_answer:
            unanswered_count += 1
            results.append({
                'question': question,
                'selected': None,
                'correct': question.correct_option,
            })
        elif selected_answer == question.correct_option:
            correct_count += 1
            results.append({
                'question': question,
                'selected': selected_answer,
                'correct': question.correct_option,
                'is_correct': True
            })
        else:
            incorrect_count += 1
            results.append({
                'question': question,
                'selected': selected_answer,
                'correct': question.correct_option,
                'is_correct': False
            })

    # Cálculo do resultado
    final_score = (correct_count * 5) - (incorrect_count * 2)

    # Enviar o resultado final
    return render(request, 'quiz/quiz_results.html', {
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'unanswered_count': unanswered_count,
        'final_score': final_score,
        'results': results,
    })
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..GPT.answer_gpt_views import answer_gpt

from ...forms import QuestionForm
from ...models import Question, QuestionHistory


@login_required(login_url='common:login')
def question_create(request):
    """
    kmuflow 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            content = question.content
            answer_gpt(request, question, content)
            return redirect('kmuflow:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'kmuflow/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''
    kmuflow 질문 수정
    '''
    question = get_object_or_404(Question, pk=question_id)
    date = question.create_date
    if question.modify_date:
        date = question.modify_date
    prevQuestion = QuestionHistory(question=question, subject=question.subject, content=question.content,
                                   modify_date=date)

    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('kmuflow:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            prevQuestion.save()
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('kmuflow:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'kmuflow/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    '''
    kmuflow 질문 삭제
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('kmuflow:detail', question_id=question.id)
    question.delete()
    return redirect('kmuflow:index')


def question_history(request, question_id):
    '''
    kmuflow 질문 수정 내역 확인
    '''
    question = get_object_or_404(Question, pk=question_id)
    question_history_list = question.questionhistory_set.all().order_by('-modify_date')
    context = {'question_history_list': question_history_list}
    return render(request, 'kmuflow/question_history.html', context)

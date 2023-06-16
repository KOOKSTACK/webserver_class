from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ...forms import AnswerForm
from ...models import Question, Answer, AnswerHistory


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    kmuflow 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('kmuflow:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'kmuflow/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    '''
    kmuflow 답변 수정
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    date = answer.create_date
    if answer.modify_date:
        date = answer.modify_date
    prevAnswer = AnswerHistory(answer=answer, content=answer.content, modify_date=date)

    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('kmuflow:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            prevAnswer.save()
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('kmuflow:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'kmuflow/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    '''
    kmuflow 답변 삭제
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        answer.delete()
    return redirect('{}#answer_{}'.format(
                resolve_url('kmuflow:detail', question_id=question.id), answer.id))


def answer_history(request, answer_id):
    '''
    kmuflow 답변 수정 내역 확인
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    answer_history_list = answer.answerhistory_set.all().order_by('-modify_date')
    context = {'answer_history_list': answer_history_list}
    return render(request, 'kmuflow/answer_history.html', context)

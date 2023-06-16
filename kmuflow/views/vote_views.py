from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from ..models import Question, Answer,Comment

@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 질문은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('kmuflow:detail', question_id=question.id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 답변은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('kmuflow:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def vote_question_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 댓글은 추천할 수 없습니다.')
    else:
        comment.voter.add(request.user)
    return redirect('kmuflow:detail', question_id= comment.question.id)

@login_required(login_url='common:login')
def vote_answer_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 댓글은 추천할 수 없습니다.')
    else:
        comment.voter.add(request.user)
    return redirect('kmuflow:detail', question_id= comment.answer.question.id)

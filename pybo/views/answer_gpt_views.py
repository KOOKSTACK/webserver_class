from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

import os
import re
import openai
import environ


from ..forms import AnswerForm
from ..models import Question, Answer, AnswerHistory

env = environ.Env(DEBUG=(bool, True)) #환경변수를 불러올 수 있는 상태로 세팅

YOUR_ORG_ID = "org-XCtzChIw6qhPLKieEBLSQhka"
OPENAI_API_KEY = env('OPENAI_API_KEY')

def gpt_connect(content):
    print("=========== GPT CONNECTING...===========")
    openai.api_key = OPENAI_API_KEY
    openai.organization = YOUR_ORG_ID
    
    model = "gpt-3.5-turbo"
    query = content
    print("=========== Quesiotn is ", query,"===========")
    
    messages = [
        {"role": "system", "content": "You are a helpful computerscience."},
        {"role": "user", "content": query}
    ]
    
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    print("=========== Waiting Answer ... ===========")
    answer = response['choices'][0]['message']['content']
    answer = "".join(answer.splitlines())
    content = {'content' : answer}
    return content


def answer_gpt(request, question_id, content):
    """
    pybo 답변 등록
    """
    print("=========== GPT ANSWER START===========")
    
    gpt =  gpt_connect(content)
    form = AnswerForm(gpt)
    if form.is_valid():
        print("==============반환된 답변 작성 중...==============")
        answer = form.save(commit=False)
        print("==============폼 저장 완료...==============")
        answer.author = request.user
        print("==============작성자 저장 완료...==============")
        answer.create_date = timezone.now()
        print("==============생성일 작성 완료...==============")
        answer.question = question_id
        print("==============답변과 연결된 질문 연결 완료...==============")
        answer.save()
        print("==============저장...==============")
    # context = {'question': question, 'form': form}
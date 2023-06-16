from django.urls import path

from .views.Comment import comment_views
from .views.Question import question_views
from .views.Answer import answer_views
from .views import base_views, vote_views



app_name = 'kmuflow'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),
    path('<int:question_id>', base_views.detail, name='detail'),

    # question_views.py
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/history/<int:answer_id>/', answer_views.answer_history, name='answer_history'),

    # answer_views.py
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>', question_views.question_delete, name='question_delete'),
    path('question/history/<int:question_id>/', question_views.question_history, name='question_history'),

    # 질문 댓글
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_quesiton,
         name='comment_create_quesiton'),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question,
         name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question,
         name='comment_delete_question'),

    # 답변 댓글
    path('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer, name='comment_delete_answer'),

    # 추천
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),
    path('vote/comment/question/<int:comment_id>/', vote_views.vote_question_comment, name='vote_question_comment'),
    path('vote/comment/answer/<int:comment_id>/', vote_views.vote_answer_comment, name='vote_answer_comment'),
    
]

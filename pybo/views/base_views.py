from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question
from ..models import Comment


def index(request):
    """
    pybo 목록 출력
    """
    page = request.GET.get("page", "1") # page
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list' : page_obj}
    # return HttpResponse("안녕하세요! pybo에 오신 것을 환영합니다!")
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question = Question.objects. get(id = question_id)
    question = get_object_or_404(Question, pk = question_id)
    
    comment_page = request.GET.get("page", "1") # 1번 page에 있는 모든 데이터
    comment_list = Comment.objects.order_by('-create_date') #-- 페이지에 잇는 모든 답변 객체리스트
    # print("comment lsit data is : " , comment_list) 
    paginator = Paginator(comment_list, 10) #-- 10개씩 
    page_obj = paginator.get_page(comment_page)
    # print("comment obj data is : " , page_obj) 흐음...
    """
    comment obj data is :  <Page 1 of 2>
    [16/May/2023 23:54:42] "GET /pybo/1?page=1 HTTP/1.1" 200 14505
    comment obj data is :  <Page 2 of 2>
    """
    context = {'question': question, 'comment_list' : page_obj, }    
    #-- 질문에 대한 정보, 페이지에 대한 정보를 넘겨준다.
    return render(request, 'pybo/question_detail.html', context)

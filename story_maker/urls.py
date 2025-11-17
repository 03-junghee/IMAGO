# story_maker/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. 시작 페이지
    path('', views.start_page, name='start'),
    
    # 2. MBTI 입력 페이지
    path('mbti/', views.mbti_input, name='mbti_input'),
    
    # 3. 질문 페이지 (핵심): question_num (1~7)을 URL 파라미터로 받습니다.
    path('q/<int:question_num>/', views.question_view, name='question'),
    
    # 4. 결과 페이지
    path('result/', views.result_page, name='result'),
]
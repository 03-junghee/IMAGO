# story_maker/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .question_data import QUESTION_DATA, CHOICE_TEXTS # 새로 만든 파일 import
from .story_generator import generate_story # 다음 단계에서 만들 파일 import

# --- 1. 시작 페이지 (기존 내용 유지) ---
def start_page(request):
    # 세션에 저장된 이전 데이터가 있으면 삭제 (설문 초기화)
    if 'mbti' in request.session:
        request.session.clear()
    return render(request, 'story_maker/start_page.html')

# --- 2. MBTI 입력 페이지 (수정: Q1로 리다이렉트) ---
def mbti_input(request):
    if request.method == 'POST':
        mbti = request.POST.get('mbti').upper()
        # 간단한 MBTI 유효성 검사 (4글자)
        if len(mbti) == 4 and all(c in 'IESNFTJP' for c in mbti):
            request.session['mbti'] = mbti 
            # 질문 1로 이동
            return redirect('question', question_num=1)
        
        return render(request, 'story_maker/mbti_input.html', {'error': '올바른 MBTI 4글자를 입력해주세요.'})
    
    return render(request, 'story_maker/mbti_input.html')


# --- 3. 질문 페이지 (핵심 로직 수정) ---
def question_view(request, question_num):
    if question_num < 1 or question_num > 7:
        return redirect('start') 

    if 'mbti' not in request.session:
        return redirect('mbti_input') 

    current_question = QUESTION_DATA.get(question_num)
    if not current_question:
        return HttpResponse("질문 데이터를 찾을 수 없습니다.", status=404)

    # ----------------------------------------------------
    # [수정] 이미지 URL을 여기서 미리 완성합니다.
    # 파일 확장자가 .png인지 다시 한번 확인해 주세요! (확장자가 다르면 여기서 수정)
    image_file_name = f'images/q{question_num}.png' 
    # ----------------------------------------------------

    if request.method == 'POST':
        # ... (POST 로직은 그대로 유지) ...
        choice = request.POST.get('choice')
        if choice and choice.isdigit():
            request.session[f'q{question_num}'] = int(choice)
            
            next_q_num = question_num + 1
            if next_q_num <= 7:
                return redirect('question', question_num=next_q_num)
            else:
                return redirect('result')
        
        context = {
            'error': '선택지를 골라주세요.',
            'question_num': question_num,
            'title': f"[ACT. {question_num}] 극이 {('시작됩니다.' if question_num == 1 else '이어집니다.')}",
            'question': current_question['question'],
            'description': current_question['description'],
            'choices': current_question['choices'],
            'image_file': image_file_name,  # [추가]
        }
        return render(request, 'story_maker/question_page.html', context)

    # GET 요청 (페이지 로드 시)
    context = {
        'question_num': question_num,
        'title': f"[ACT. {question_num}] 극이 {('시작됩니다.' if question_num == 1 else '이어집니다.')}",
        'question': current_question['question'],
        'description': current_question['description'],
        'choices': current_question['choices'],
        'image_file': image_file_name, # [추가]
    }
    return render(request, 'story_maker/question_page.html', context)


# --- 4. 결과 페이지 (generate_story 함수가 필요함) ---
def result_page(request):
    # 모든 질문에 응답했는지 확인 (q1부터 q7까지 모두 있어야 함)
    for i in range(1, 8):
        if f'q{i}' not in request.session:
            # 응답이 불완전하면 마지막 질문으로 돌려보냅니다.
            return redirect('question', question_num=7) 

    # story_generator.py의 함수를 사용하여 소설 텍스트와 통계를 생성합니다.
    story_text, choice_stats = generate_story(request.session) 
    
    context = {
        'mbti': request.session.get('mbti'),
        'story_text': story_text,
        'stats': choice_stats,
    }
    
    # DB 저장 로직은 현재 생략 (SQLite3 임시 사용), 필요하면 나중에 추가
    
    return render(request, 'story_maker/result_page.html', context)
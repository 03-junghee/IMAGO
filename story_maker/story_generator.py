# story_maker/story_generator.py

from .question_data import CHOICE_TEXTS

# ----------------------------------------------------------------------
# [추가] 한국어 조사 '을/를'을 선택하는 함수
# ----------------------------------------------------------------------
def get_josa_ul_leul(word):
    """
    단어의 마지막 글자에 받침이 있으면 '을', 없으면 '를'을 반환합니다.
    """
    if not word:
        return '을'  # 입력이 비어있으면 기본값 반환
    
    # Python 3에서 유니코드 마지막 글자의 종성(받침)을 확인
    last_char = word[-1]
    
    # 한글 유니코드 범위: 44032 (가) ~ 55203 (힣)
    if '가' <= last_char <= '힣':
        # (유니코드 코드 포인트 - 44032) % 28
        # 이 결과가 0이면 받침 없음 (종성 없음), 0이 아니면 받침 있음
        if (ord(last_char) - 44032) % 28 == 0:
            return '를'  # 받침 없음
        else:
            return '을'  # 받침 있음
    else:
        # 한글이 아닌 경우 (예: 숫자, 기호)
        return '를' # 받침이 없다고 가정하고 '를' 반환
# ----------------------------------------------------------------------

# MBTI 유형에 따른 특징 정의 (첫 문장에 사용)
MBTI_FEELINGS = {
    'E': '새로운 하루에 대한 기대감과 함께 활기가 넘쳤습니다.',
    'I': '평소와 다름없는 평온함 속에서 내면의 생각을 정리하고 있었습니다.',
    'N': '어젯밤 꾸었던 꿈의 잔상을 곱씹으며 상상의 나래를 펼치고 있었습니다.',
    'S': '오늘 해야 할 일들을 빠르게 스캔하며 현실적인 준비를 하고 있었습니다.',
    'F': '몸은 피곤했지만 마음만은 따뜻하게, 주변 사람들의 안부를 떠올리고 있었습니다.',
    'T': '복잡한 머리를 식힐 새도 없이, 문제 해결을 위한 논리적인 생각에 잠겨 있었습니다.',
    'J': '정확히 계획된 일과를 시작해야 한다는 책임감과 압박감이 느껴졌습니다.',
    'P': '이 순간의 자유로움을 만끽하며, 오늘의 일은 오늘의 기분에 맡기기로 했습니다.',
}

# [추가] MBTI의 나머지 3가지 특성을 묘사하는 텍스트
MBTI_SCENE_INSERTS = {
    # 2번째 자리 (S/N): 이동 중 생각
    'N': '상상력이 풍부한 당신은 이동 내내 기묘한 생각에 사로잡혔습니다.',
    'S': '현실적인 당신은 이동 중에도 주변의 구체적인 정보를 놓치지 않았습니다.',

    # 3번째 자리 (T/F): 점심 식사 후 감정
    'T': '식사 후, 당신은 곧바로 남은 일정을 논리적으로 분석하며 효율을 극대화했습니다.',
    'F': '식사 후, 당신은 주변 사람들의 표정이나 분위기를 살피며 공감의 시간을 가졌습니다.',

    # 4번째 자리 (J/P): 저녁 일과를 대하는 태도
    'J': '체계적인 당신은 하루가 끝나기 전에 모든 할 일 목록을 점검하는 습관을 보였습니다.',
    'P': '유연한 당신은 계획에 얽매이지 않고, 그때그때 떠오르는 생각에 따라 행동하며 시간을 보냈습니다.',
}

# --- 소설 생성 함수 ---
def generate_story(session_data):
    mbti = session_data.get('mbti', '____')
    
    # MBTI 4자리 특성 추출 (오류 방지 위해 길이 확인)
    if len(mbti) != 4:
        # MBTI가 4글자가 아닐 경우 기본값 설정
        mbti_parts = ['I', 'S', 'T', 'P']
    else:
        mbti_parts = list(mbti)

    E_I, S_N, T_F, J_P = mbti_parts

    # MBTI별 묘사 텍스트 가져오기
    mbti_feeling_text = MBTI_FEELINGS.get(E_I, MBTI_FEELINGS['I']) # E/I
    s_n_insert = MBTI_SCENE_INSERTS.get(S_N, MBTI_SCENE_INSERTS['S']) # S/N
    t_f_insert = MBTI_SCENE_INSERTS.get(T_F, MBTI_SCENE_INSERTS['T']) # T/F
    j_p_insert = MBTI_SCENE_INSERTS.get(J_P, MBTI_SCENE_INSERTS['P']) # J/P

    # 1. 선택지 텍스트 가져오기
    answers = {}
    for i in range(1, 8):
        q_key = f'q{i}'
        choice_num = session_data.get(q_key, 0)
        answers[q_key] = CHOICE_TEXTS[q_key].get(choice_num, '선택되지 않은 상황')

    # 2. 소설 프레임 채우기 (조사 적용)
    
    # [수정] q2, q3 단어에 맞는 조사를 계산
    josa_q2 = get_josa_ul_leul(answers['q2']) # 자가용 + 을/를
    josa_q3 = get_josa_ul_leul(answers['q3']) # 오마카세 + 을/를
    
    story = (
        f"[당신의 하루 - 단막극]\n\n"
        f"나는 {answers['q1']}에서 눈을 떴습니다. 눈을 뜨자마자 느껴지는 이 감정은 {mbti_feeling_text}\n\n"
        
        # [S/N 특성 삽입]
        f"어찌 됐든 {answers['q2']}{josa_q2} 이용하여 오늘의 일과를 시작한 나는, {s_n_insert} 낮 12시가 되었습니다.\n\n"
        
        # [T/F 특성 삽입]
        f"{answers['q3']}{josa_q3} 먹으며 짧은 휴식을 취한 당신은, {t_f_insert}\n\n"
        
        f"그때 울리는 휴대폰. {answers['q4']}에게 '{answers['q5']}' 때문에 연락이 왔습니다. 연락을 확인한 당신은 잠시 복잡한 생각에 잠겼습니다.\n\n"
        
        # [J/P 특성 삽입]
        f"모든 일과를 마치고 잠자리에 들기 전, {j_p_insert} 당신은 '{answers['q6']}'하며 하루를 정리합니다. 그런데 아뿔싸, 잠이 오지 않아 결국 '{answers['q7']}'를 선택하며 길었던 하루의 막을 내립니다.\n\n"
        
        f"이 모든 당신의 선택이 IMAGO AI가 형상화한 당신의 이야기입니다."
    )
    
    # 4. 통계 계산 (MBTI와 일치하는 선택 카운트 - 예시)
    stats = {}
    
    # F/T 비율 통계 (Q4, Q5 감정/논리적 선택을 가정한 통계)
    # Q4: 1, 2, 3 (F성향), 4 (T성향)
    # Q5: 1, 2, 4 (F성향), 3 (T성향)
    t_count = 0
    f_count = 0
    if answers['q4'] == CHOICE_TEXTS['q4'][4]: t_count += 1
    if answers['q5'] == CHOICE_TEXTS['q5'][3]: t_count += 1
    if answers['q4'] != CHOICE_TEXTS['q4'][4]: f_count += 1
    if answers['q5'] != CHOICE_TEXTS['q5'][3]: f_count += 1

    stats['F_T_ratio'] = {
        'T_count': t_count,
        'F_count': f_count,
        'mbti_T_F': 'T' if 'T' in mbti[2] else 'F'
    }

    return story, stats
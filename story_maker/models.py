from django.db import models

class UserResponse(models.Model):
    # 기본 정보
    session_id = models.CharField(max_length=100, unique=True, help_text="세션 또는 임시 ID")
    mbti = models.CharField(max_length=4, verbose_name="MBTI 유형")
    
    # 각 질문의 응답 (1~7)
    q1_location = models.IntegerField(verbose_name="Q1. 기상 장소")
    q2_transport = models.IntegerField(verbose_name="Q2. 이동 수단")
    q3_lunch = models.IntegerField(verbose_name="Q3. 점심 식사")
    q4_contact = models.IntegerField(verbose_name="Q4. 연락한 사람")
    q5_reason = models.IntegerField(verbose_name="Q5. 연락 이유")
    q6_bedtime_thought = models.IntegerField(verbose_name="Q6. 취침 전 생각")
    q7_sleepless = models.IntegerField(verbose_name="Q7. 잠 안 올 때 대처")
    
    # 제출 시간 기록
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mbti} - {self.session_id}"
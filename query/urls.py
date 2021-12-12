from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.conf import settings


urlpatterns = [
    path('mentor_register/', RegisterMentor.as_view(), name='mentor_register'),
    path('student_register/', RegisterStudent.as_view(), name='student_register'),
    path('user_login/', Userlogin.as_view(), name='user_login'),
    path('post_question/', PostQuestion.as_view(), name='post_question'),
    path('all_questions/', ListQuestionView.as_view(), name='all_questions'),
    path('question_reply/', ReplyQuestionPOSTView.as_view(), name='question_reply'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
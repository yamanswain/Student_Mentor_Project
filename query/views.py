import datetime
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .tokens import generate_jwt_token
from .models import *
from .serializer import RegistrationSerializer,MentorSerializer,QuestionSerializer


import logging
logger = logging.getLogger(__name__)


class RegisterMentor(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
                      This API use for RegisterMentor
                      Request parameter:->{"email": "yaman@gmail.com",
                                          "password": "yAman@!@#2",
                                          "password2": "yAman@!@#2",
                                          "role": "mentor"
                                          }
                      RETURN:->
                      {
                      "message": "User registered successfully",
                      "status": 200,
                      "result": {
                          "email": "yaman@gmail.com",
                          "role": "mentor"
                          }
                      }

                  """
        logger_user_id = self.request.META['REMOTE_ADDR']
        logger.debug("[" + str(logger_user_id) + "][RegisterMentor][POST]Entered" + f'Request Parameter:{request.data}')
        try:
            role = self.request.data.get("role", None)
            if role:
                if role == "mentor":
                    serializer = MentorSerializer(data=request.data)
                    if serializer.is_valid():
                        user = serializer.save()
                        return Response({"message": "SUCCESS_REGISTERED_SUCCESSFULLY","status": status.HTTP_200_OK,
                                         "result": {"email": user.email, "role": user.role}}, status=status.HTTP_200_OK)
                    else:
                        error_list = [serializer.errors[error][0] for error in serializer.errors][0]
                        return Response({"message": error_list, "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "PROVIDE_CORRECT_ROLE", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "PROVIDE_CORRECT_ROLE", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("[" + logger_user_id + "][RegisterMentor][GET]Error Occurred " + str(e))
            return Response({"message": "ERROR_TECHNICAL", "status": status.HTTP_400_BAD_REQUEST},
							status=status.HTTP_400_BAD_REQUEST)


class RegisterStudent(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
            This API use for RegisterStudent
            Request parameter:-> {
                                "student_email": "k.yaman@gmail.com",
                                "password": "Yaman@!12",
                                "password2": "Yaman@!12",
                                "mentor_email": "yaman.k@gmail.com",
                                "role": "student"
                                }
            RETURN:->
            {
            "message": "User registered successfully",
            "status": 200,
            "result": {
                "email": "k.yaman@gmail.com",
                "role": "student"
                }
            }

        """
        logger_user_id = self.request.META['REMOTE_ADDR']
        logger.debug("[" + str(logger_user_id) + "][RegisterStudent][POST]Entered" + f'Request Parameter:{request.data}')
        try:
            role = self.request.data.get("role", None)
            if self.request.user.is_authenticated:
                if role == "student":
                    value = None
                    if role == "student":
                        value = RegistrationSerializer
                    if value:
                        email = self.request.data.get("mentor_email", None)
                        mentor = Mentor.objects.get(email=email)
                        data = {"mentor": mentor.pk,
                                "email": self.request.data.get("student_email"),
                                "password": self.request.data.get("password"),
                                "password2": self.request.data.get("password2"),
                                "mentor_email": email,
                                "role": "student"}
                        serializer = value(data=data)
                        if serializer.is_valid():
                            user = serializer.save()
                            return Response({"message": "SUCCESS_REGISTERED_SUCCESSFULLY", "status": status.HTTP_200_OK,
                                             "result": {"email": user.email, "role": user.role}},
                                            status=status.HTTP_200_OK)
                        else:
                            error_list = [serializer.errors[error][0] for error in serializer.errors][0]
                            return Response({"message": error_list, "status": status.HTTP_400_BAD_REQUEST},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(
                            {"message": "PROVIDE_CORRECT_ROLE_STUDENT", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "PROVIDE_CORRECT_ROLE_STUDENT", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "LOGIN_FIRST", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("[" + logger_user_id + "][RegisterStudent][POST]Error Occurred " + str(e))
            return Response({"message": "ERROR_TECHNICAL", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)


class Userlogin(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
                This API use for Userlogin
                Request parameter:-> {
                                    "email": "yaman83@gmail.com",
                                    "password": "yaman@!2",
                                    "role": "mentor"
                                    }
                RETURN:->
                    {
                    "message": "User logged in successfully",
                    "status": 200,
                    "result": {
                    "user_email": "yaman83@gmail.com",
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNjM5NjYxNzQwfQ.k9dTYLgIZ1juwn-DxOl_ZR85U7R1tHoS3kj8KQ3akXQ",
                    "login_time": "09 Dec 2021 13:35 PM",
                    "registration_date": "09 Dec 2021 09:56 AM"
                    }
                }
            """
        logger_user_id = self.request.META['REMOTE_ADDR']
        logger.debug("[" + str(logger_user_id) + "][Userlogin][POST]Entered" + f'Request Parameter:{request.data}')
        try:
            email = self.request.data.get("email", None)
            password = self.request.data.get("password", None)
            role = self.request.data.get("role", None)
            if email and password:
                value = None
                if role == "mentor":
                    value = Mentor
                elif role == "student":
                    value = Student
                if value:
                    try:
                        user = value.objects.get(email=email)
                        if check_password(password, user.password):
                            auth.login(request, user)
                            data = {"user_email": user.email, "token": generate_jwt_token(user), "login_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    "registration_date": user.registration_date.strftime('%Y-%m-%d %H:%M:%S')}
                            return Response({"message": "LOGGED_SUCCESSFULLY", "status": status.HTTP_200_OK,
                                             "result": data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"message": "INVALID_PASSWORD", "status": status.HTTP_400_BAD_REQUEST},
                                            status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        logger.error("[" + logger_user_id + "][User_login][POST]Error Occurred " + str(e))
                        return Response({"message": "INVALID_USERNAME", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "CHECK_PERMISSION_ROLE", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "REQUEST_PARAMETER", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("[" + logger_user_id + "][Userlogin][POST]Error Occurred " + str(e))
            return Response({"message": "ERROR_TECHNICAL", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)


class ListQuestionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
                This API use for ListQuestionView
                Request parameter:-> {
                                        "email": "yaman123@gmail.com"
                                        "role": "mentor"
                                    }
                RETURN:->
                {
                    "message": "Data Retrieved successfully",
                    "status": 200,
                    "result": [
                            {
                            "student_email": "yaman123@gmail.com",
                            "mentor_email": "yaman@gmail.com",
                            "question": "what is Meta data",
                            "reply": null,
                            "attachment_name": null
                            },
                            {
                            "student_email": "yaman123@gmail.com",
                            "mentor_email": "yaman@gmail.com",
                            "question": "data about data",
                            "reply": null,
                            "attachment_name": null
                            },
                            {
                            "student_email": "yaman123@gmail.com",
                            "mentor_email": "yaman@gmail.com",
                            "question": "Good questions",
                            "reply": null,
                            "attachment_name": null
                            }
                        ]
                }
                        """
        logger_user_id = self.request.META['REMOTE_ADDR']
        logger.debug("[" + str(logger_user_id) + "][ListQuestionView][POST]Entered" + f'Request Parameter:{request.data}')
        try:
            email = self.request.data.get("email", None)
            role = self.request.data.get("role", None)
            if self.request.user.is_authenticated:
                questions = None
                if role == "mentor":
                    mentor = Mentor.objects.get(email=email)
                    questions = Question.objects.filter(mentor=mentor)
                elif role == "student":
                    user = Student.objects.get(email=email)
                    questions = Question.objects.filter(user=user)
                if questions:
                    question_list = []
                    for question in questions:
                        data = {"student_email": question.user.email, "mentor_email": question.mentor.email,
                                "question": question.question, "reply": question.reply, "attachment_name": question.file_name}
                        question_list.append(data)
                    if question_list:
                        return Response({"message": "SUCCESS_DATA_RETRIEVED", "status": status.HTTP_200_OK,
                                         "result": question_list}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "DATA_NOT_FOUND", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "NO_DATA_ASSOCIATED", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "LOGIN_FIRST", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("[" + logger_user_id + "][ListQuestionView][POST]Error Occurred " + str(e))
            return Response({"message": "ERROR_TECHNICAL", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)


class PostQuestion(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
                This API use for PostQuestion
                Request parameter:-> {
                                     "student_email": "yaman345@gmail.com",
                                    "mentor_email": "yaman.k@gmail.com",
                                    "question": "What is Meta data",
                                    "message": ""
                 }
                RETURN:->
                {
                 "message": "Query saved successfully",
                "status": 200,
                "result": {
                        "question": "Good questions",
                        "student_email": "yaman345@gmail.com",
                        "mentor_email": "yaman.k@gmail.com"
                        }
                }
        """
        logger_user_id = self.request.META['REMOTE_ADDR']
        logger.debug("[" + str(logger_user_id) + "][PostQuestion][POST]Entered" + f'Request Parameter:{request.data}')
        try:
            student_email = self.request.data.get("student_email", None)
            mentor_email = self.request.data.get("mentor_email", None)
            question = self.request.data.get("question", None)
            message = self.request.data.get("message", None)
            file = self.request.FILES.get("file", None)
            if self.request.user.is_authenticated:
                if student_email and question:
                    try:
                        user = Student.objects.get(email=student_email)
                        mentor = Mentor.objects.get(email=mentor_email)
                        dict_value = {"mentor": mentor.pk, "user": user.pk, "question": question, "message": message,
                                     "reply": None, "file_name": file.name if file else None,
                                     "file": file, "post_time": datetime.now(), "replied_time": None}
                        serializer = QuestionSerializer(data=dict_value)
                        if serializer.is_valid():
                            data = serializer.save()
                            return Response({"message": "SAVED_SUCCESSFULLY", "status": status.HTTP_200_OK,
                                             "result": {"question": data.question, "student_email": data.user.email,
                                                "mentor_email": data.mentor.email }}, status=status.HTTP_200_OK)
                        else:
                            error_list = [serializer.errors[error][0] for error in serializer.errors][0]
                            return Response({"message": error_list, "status": status.HTTP_400_BAD_REQUEST},
                                            status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        logger.error("[" + logger_user_id + "][post_question][POST]Error Occurred " + str(e))
                        return Response({"message": "USER_NOT_FOUND", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "REQUEST_PARAMETER", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "LOGIN_FIRST", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("[" + logger_user_id + "][PostQuestion][POST]Error Occurred " + str(e))
            return Response({"message": "ERROR_TECHNICAL", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)


class ReplyQuestionPOSTView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        """
                    This API use for ReplyQuestionPOSTView
                    Request parameter:-> {
                                "student_email": "yaman@gmail.com",
                                "mentor_email": "yaman.k@gmail.com",
                                "question": "What is Meta data",
                                "reply": "Data about data",
                                "role": "mentor",
                                "message": ""

                                }
                    RETURN:->
                    {
                     "message": "Query saved successfully",
                    "status": 200,
                    "result": {
                                ""

                                }
                    }
            """
        logger_user_id = self.request.META['REMOTE_ADDR']
        logger.debug("[" + str(logger_user_id) + "][ReplyQuestionPOSTView][POST]Entered" + f'Request Parameter:{request.data}')
        try:
            student_email = self.request.data.get("student_email") or None
            mentor_email = self.request.data.get("mentor_email") or None
            question = self.request.data.get("question") or None
            reply = self.request.data.get("reply") or None
            role = self.request.data.get("role") or None
            message = self.request.data.get("message") or None
            file = self.request.FILES.get("file") or None
            if self.request.user.is_authenticated:
                if role == "mentor":
                    if student_email and mentor_email and question and reply:
                        try:
                            user = Student.objects.get(email=student_email)
                            mentor = Mentor.objects.get(email=mentor_email)
                            question_data = Question.objects.get(user=user, mentor=mentor, question__exact=question)
                            question_data.reply = reply
                            question_data.message = message
                            question_data.reply_time = datetime.now()
                            question_data.file_name = file.name if file else None
                            question_data.file = file
                            question_data.save()
                            return Response({"message": "REPLIED_SUCCESSFULY", "status": status.HTTP_200_OK,
                                             "result": {"student": user.email, "mentor": mentor.email, "question": question,
                                                "reply": reply}}, status=status.HTTP_200_OK)
                        except Exception as e:
                            logger.error("[" + logger_user_id + "][questions_reply][POST]Error Occurred " + str(e))
                            return Response({"message": "USER_NOT_FOUND", "status": status.HTTP_400_BAD_REQUEST},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"message": "REQUEST_PARAMETERS ARE MISSING", "status": status.HTTP_400_BAD_REQUEST},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "CAN_NOT_REPLY_QUESTIONS", "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "LOGIN_FIRST", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("[" + logger_user_id + "][ReplyQuestionPOSTView][POST]Error Occurred " + str(e))
            return Response({"message": "ERROR_TECHNICAL", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
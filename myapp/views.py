

# Create your views here.
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSignupSerializer
from .models import User
from .models import QuizQuestion
from django.shortcuts import render
import json
import hashlib  # Only for demo hashing (not recommended for production)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User  # assuming custom User model maps to `Users` table
from .serializers import UserLoginSerializer
from .serializers import QuestionCreateSerializer
from .serializers import QuestionListSerializer
from .models import Question
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Quiz, QuizQuestion
from .models import StudentExam, Answer
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question
# import openai
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from transformers import pipeline
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os

from .serializers import QuizListSerializer
from .models import ParentStudentMapping


# # Load model globally once
# qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")


# Optional: You can change this to a custom passage or context
default_context = """
Mathematics is the study of numbers, shapes, and patterns. It is used in everything from engineering and architecture to economics and data science.
The Pythagorean theorem states that in a right-angled triangle, a² + b² = c².
The derivative of sin(x) is cos(x). The area of a circle is πr².
Mean is the average of a data set.
Median is the middle value of a data set when it is arranged in order.
Mode is the value that appears most frequently in a data set.
"""

from django.http import JsonResponse

# Optimize Initial Load 
def health_check(request):
    return JsonResponse({'status': 'ok'})


def user_registration(request):
    return render(request, 'pages/user_registration.html')  # Updated path


def home(request):
    return HttpResponse("Hello, Django is working!")




@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        else:
            # Log the validation errors for debugging
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import User

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        data = request.data

        # Update fields if present in the request
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.firstName = data.get('firstName', user.firstName)
        user.lastName = data.get('lastName', user.lastName)

        # Update fullName automatically if first/last changed
        user.fullName = f"{user.firstName} {user.lastName}"

        if 'password' in data and data['password']:
            user.password = make_password(data['password'])

        user.role = data.get('role', user.role)
        user.academicLevel = data.get('academicLevel', user.academicLevel)
        user.userStatus = data.get('userStatus', user.userStatus)

        user.save()

        return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def user_login(request):
    # email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    #hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        # user = User.objects.get(email=email)
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            
            # Generate JWT token on successful login
            refresh = RefreshToken.for_user(user)
            # access_token = str(refresh.access_token)
            access_token = refresh.access_token
            access_token['username'] = user.username
            access_token['fullName'] = user.fullName
            access_token['role'] = user.role



            return Response({
                'message': 'Login successful',
                'username': user.username,
                'role': user.role,
                'status': user.userStatus,
                # 'token': access_token
                'token': str(access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def create_question(request):
    serializer = QuestionCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Question created successfully!'}, status=status.HTTP_201_CREATED)
    # Log the validation errors for debugging
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_all_users(request):
    users = User.objects.all()
    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "fullName": user.fullName,
            "role": user.role,
            "academicLevel": user.academicLevel,
            "userStatus": user.userStatus
        })

    return Response(user_list)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def list_questions(request):
    questions = Question.objects.all()
    serializer = QuestionListSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_questions(request):
    questions = Question.objects.all()

    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty_level')

    if category:
        questions = questions.filter(category__iexact=category)
    if difficulty:
        questions = questions.filter(difficulty_level__iexact=difficulty)

    # serializer = QuestionCreateSerializer(questions, many=True)
    serializer = QuestionListSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_quiz(request):
    data = request.data
    username = data.get("username")
    quiz_title = data.get("quizName")
    quiz_level = data.get("quizLevel")
    quiz_status = data.get("quizStatus", "draft")
    selected_questions = data.get("selectedQuestions", [])

    if not username or not quiz_title or not selected_questions:
        return Response({"error": "Missing required fields"}, status=400)

    for q in selected_questions:
        if "score" not in q or "questionId" not in q:
            return Response({"error": "Each selected question must include 'score' and 'questionId'."}, status=400)

    try:
        user = User.objects.get(username=username)
        teacher_id = user.id
        total_marks = sum(int(q.get("score", 0)) for q in selected_questions)

        with connection.cursor() as cursor:
            # Insert the quiz and return its ID
            cursor.execute("""
                INSERT INTO quiz (teacher_id, quiz_title, quiz_level, quiz_status, total_marks, created_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING quiz_id
            """, [teacher_id, quiz_title, quiz_level, quiz_status, total_marks])

            quiz_id = cursor.fetchone()[0]  # Get generated ID

            # Insert each selected question
            for q in selected_questions:
                question_id = q["questionId"]
                score = int(q["score"])
                cursor.execute(
                    "INSERT INTO quiz_questions (quiz_id, question_id, score) VALUES (%s, %s, %s)",
                    [quiz_id, question_id, score]
                )

        return Response({"message": "Quiz created successfully!", "quiz_id": quiz_id}, status=201)

    except User.DoesNotExist:
        return Response({"error": "Invalid username"}, status=404)
    except Exception as e:
        print("Error:", str(e))
        return Response({"error": str(e)}, status=500)


@api_view(['PUT'])
def update_question(request, question_id):
    try:
        question = Question.objects.get(question_id=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    question.question_text = data.get('text', question.question_text)
    question.difficulty_level = data.get('level', question.difficulty_level)
    question.category = data.get('category', question.category)
    question.correct_answer = data.get('correctAnswer', question.correct_answer)

    try:
        question.save()
        return Response({'message': 'Question updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_question(request, question_id):
    try:
        question = Question.objects.get(question_id=question_id)
        question.delete()
        return Response({'message': 'Question deleted successfully'}, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Configure OpenAI with your API key
# openai.api_key = settings.OPENAI_API_KEY


# import openai
# from openai import OpenAI

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# @api_view(['POST'])
# def ask_ai(request):
#     question = request.data.get("question")

#     if not question:
#         return Response({'error': 'No question provided'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         result = qa_pipeline({
#             'context': default_context,
#             'question': question
#         })

#         return Response({'answer': result['answer']})
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import traceback
import requests

@csrf_exempt
@api_view(['POST'])
def ask_ai(request):
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
    if not TOGETHER_API_KEY:
        return Response({'error': 'Together API key not set'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    question = request.data.get("question")
    if not question:
        return Response({'error': 'No question provided'}, status=status.HTTP_400_BAD_REQUEST)

    print("Question:", question)

    try:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        # Inject default context into the user prompt (simple RAG)
        user_prompt = f"{default_context}\n\nQuestion: {question}"

        payload = {
            # "model": "togethercomputer/llama-2-7b-chat",
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {"role": "system", "content": "You are a helpful math tutor. Use the provided context to assist the student."},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512,
            "top_p": 0.95,
        }

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        return Response({'answer': answer})

    except requests.exceptions.HTTPError as e:
        print("HTTP ERROR:", e.response.text)
        return Response({'error': 'HTTP Error from Together.ai'}, status=status.HTTP_502_BAD_GATEWAY)
    except Exception as e:
        print("EXCEPTION:", str(e))
        traceback.print_exc()
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_all_quizzes(request):
    quizzes = Quiz.objects.select_related('teacher').all().order_by('-created_at')
    serializer = QuizListSerializer(quizzes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        return Response({"error": "Quiz not found."}, status=404)

    data = request.data

    quiz.quiz_title = data.get("quiz_title", quiz.quiz_title)
    quiz.quiz_status = data.get("quiz_status", quiz.quiz_status)
    quiz.quiz_level = data.get("quiz_level", quiz.quiz_level)
    # Add any other fields here

    quiz.save()
    return Response({"message": "Quiz updated successfully!"}, status=200)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, QuizQuestion
import ast  # For safely evaluating stringified list

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, QuizQuestion
import ast

@api_view(['POST'])
def attend_quiz(request):
    quiz_name = request.data.get('quiz_name')
    quiz_level = request.data.get('quiz_level')
    category = request.data.get('category')

    if not quiz_name or not quiz_level or not category:
        return Response({'error': 'quiz_name, quiz_level, and category are required'}, status=400)

    try:
        quiz = Quiz.objects.get(quiz_title=quiz_name, quiz_level=quiz_level)
        quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question')

        filtered_questions = []
        for qq in quiz_questions:
            if qq.question.category.lower() == category.lower():
                try:
                    options = ast.literal_eval(qq.question.answers)
                except:
                    options = []

                filtered_questions.append({
                    "questionId": qq.question.question_id,
                    "question": qq.question.question_text,
                    "options": options
                })

        if not filtered_questions:
            return Response({'error': 'No questions found for selected category and level.'}, status=404)

        return Response({'quiz': filtered_questions}, status=200)

    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found.'}, status=404)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def submit_quiz(request):
    username = request.data.get('username')
    quiz_name = request.data.get('quiz_name')
    quiz_level = request.data.get('quiz_level')
    answers = request.data.get('answers')

    if not all([username, quiz_name, quiz_level, answers]):
        return Response({'error': 'Missing fields'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    # ✅ Use filter + first to avoid MultipleObjectsReturned error
    quiz = Quiz.objects.filter(
        quiz_title=quiz_name,
        quiz_level=quiz_level,
        quiz_status='published'  # Optional: only allow published quizzes
    ).order_by('-created_at').first()

    if not quiz:
        return Response({'error': 'Quiz not found'}, status=404)

    try:
        quiz_questions = QuizQuestion.objects.filter(quiz=quiz).select_related('question')

        # Create the exam record
        exam = StudentExam.objects.create(student=user, quiz=quiz, score=0)

        score = 0

        for qq in quiz_questions:
            question = qq.question
            qid_str = str(question.question_id)
            user_answer = answers.get(qid_str, "").strip().lower()
            correct_answer = question.correct_answer.strip().lower()

            # 🧠 Debug logs
            print(f"[DEBUG] Question ID: {qid_str}")
            print(f"[DEBUG] Submitted Answer: '{user_answer}'")
            print(f"[DEBUG] Correct Answer:   '{correct_answer}'")

            is_correct = user_answer == correct_answer

            if is_correct:
                score += 1
                print(f"[DEBUG] -> Answer is correct.")
            else:
                print(f"[DEBUG] -> Answer is incorrect.")

            Answer.objects.create(
                student_exam=exam,
                question=question,
                student_answer=user_answer,
                is_correct=is_correct
            )

        exam.score = score
        exam.save()

        print(f"[DEBUG] Final Score for {user.username}: {score}")

        return Response({
            'message': 'Quiz submitted successfully',
            'score': score,
            'total_questions': quiz_questions.count()
        }, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def publish_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
        quiz.quiz_status = 'published'
        quiz.save()
        return Response({'message': 'Quiz published successfully!'}, status=200)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found.'}, status=404)

@api_view(['DELETE'])
def delete_quiz(request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            quiz.delete()
            return Response({'message': 'Quiz deleted successfully'}, status=200)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



@api_view(['GET'])
def view_result(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        exams = StudentExam.objects.filter(student=user).select_related('quiz')

        result = []

        for exam in exams:
            answers = Answer.objects.filter(student_exam=exam).select_related('question')
            answer_data = []

            for a in answers:
                try:
                    answer_data.append({
                        "question_id": a.question.question_id,
                        "question_text": a.question.question_text,
                        "student_answer": a.student_answer,
                        "is_correct": a.is_correct,
                        "mark": getattr(a, 'student_mark', None),
                        "comment": getattr(a, 'teacher_comment', None)
                    })
                except Exception as e:
                    print(f"[ERROR] Skipping broken answer record (Answer ID: {a.answer_id}): {str(e)}")

            result.append({
                "quiz_title": exam.quiz.quiz_title,
                "quiz_level": exam.quiz.quiz_level,
                "score": exam.score,
                "taken_at": exam.taken_at,
                "answers": answer_data
            })

        return Response(result, status=200)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)



@api_view(['POST'])
def evaluate_quiz(request):
    data = request.data
    username = data.get('username')
    quiz_name = data.get('quiz_name')
    quiz_level = data.get('quiz_level')
    evaluations = data.get('evaluations')

    if not all([username, quiz_name, quiz_level, evaluations]):
        return Response({'error': 'Missing fields'}, status=400)

    try:
        user = User.objects.get(username=username)
        quiz = Quiz.objects.filter(
            quiz_title=quiz_name,
            quiz_level=quiz_level
        ).order_by('-created_at').first()

        if not quiz:
            return Response({'error': 'Quiz not found'}, status=404)

        exam = StudentExam.objects.filter(student=user, quiz=quiz).order_by('-taken_at').first()

        if not exam:
            return Response({'error': 'Exam not found'}, status=404)

        total_score = 0

        for qid, eval_data in evaluations.items():
            question = Question.objects.get(question_id=int(qid))
            answer = Answer.objects.get(student_exam=exam, question=question)

            answer.student_mark = eval_data.get('mark', 0)
            answer.teacher_comment = eval_data.get('comment', '')
            answer.save()

            total_score += answer.student_mark

        exam.score = total_score
        exam.save()

        return Response({'message': 'Evaluation saved', 'score': total_score}, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)

# Used for user registration

@api_view(['GET'])
def get_user_by_username(request, username):
    try:
        user = User.objects.get(username=username)
        return Response({'user': {
            'username': user.username,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'academicLevel': user.academicLevel,
            'userStatus': user.userStatus,
            'role': user.role
        }})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

        @api_view(['GET'])
def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query)
    return Response({'users': list(users.values())})

#  Get assigned students for a parent

@api_view(['GET'])
def get_assigned_students(request, username):
    try:
        parent = User.objects.get(username=username, role='parent')
        mappings = ParentStudentMapping.objects.filter(parent=parent)
        students = [{"username": m.student.username, "fullName": m.student.fullName} for m in mappings]
        return Response({"students": students})
    except User.DoesNotExist:
        return Response({"error": "Parent not found"}, status=404)

# Assign a student to a parent

@api_view(['POST'])
def assign_student(request, username):
    student_username = request.data.get("student_username")
    print(f"Trying to assign student {student_username} to parent {username}")

    try:
        parent = User.objects.get(username=username, role='parent')
        student = User.objects.get(username=student_username, role='student')

        if ParentStudentMapping.objects.filter(parent=parent, student=student).exists():
            return Response({"message": "Student already assigned to this parent."})

        ParentStudentMapping.objects.create(parent=parent, student=student)
        return Response({"message": f"{student.username} assigned to {parent.username}."})
    except Exception as e:
        print("Error during assignment:", str(e))  # Log the real cause
        return Response({"error": str(e)}, status=500)


@api_view(['DELETE'])
def remove_assigned_student(request, parent_username, student_username):
    try:
        parent = User.objects.get(username=parent_username, role='parent')
        student = User.objects.get(username=student_username, role='student')

        mapping = ParentStudentMapping.objects.filter(parent=parent, student=student).first()

        if mapping:
            mapping.delete()
            return Response({'message': f'Student {student_username} removed from parent {parent_username}.'}, status=200)
        else:
            return Response({'message': 'Mapping does not exist.'}, status=404)

    except User.DoesNotExist:
        return Response({'message': 'Parent or student not found.'}, status=404)
    except Exception as e:
        return Response({'message': f'Error: {str(e)}'}, status=500)

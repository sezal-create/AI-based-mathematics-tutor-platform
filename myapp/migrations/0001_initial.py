# Generated by Django 5.1.7 on 2025-04-29 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AIQuiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('Arithmetic', 'Arithmetic'), ('Trigonometry', 'Trigonometry'), ('Algebra', 'Algebra'), ('Geometry', 'Geometry'), ('Calculus', 'Calculus')], max_length=50)),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=10)),
                ('ai_generated', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('Arithmetic', 'Arithmetic'), ('Trigonometry', 'Trigonometry'), ('Algebra', 'Algebra'), ('Geometry', 'Geometry'), ('Calculus', 'Calculus')], max_length=50)),
                ('question_text', models.TextField()),
                ('ansType', models.TextField()),
                ('answers', models.TextField()),
                ('correct_answer', models.CharField(max_length=255)),
                ('difficulty_level', models.CharField(choices=[('kindergartens', 'kindergartens'), ('year_1', 'year_1'), ('year_2', 'year_2'), ('year_3', 'year_3'), ('year_4', 'year_4'), ('year_5', 'year_5'), ('year_6', 'year_6'), ('year_7', 'year_7'), ('year_8', 'year_8'), ('year_9', 'year_9'), ('year_10', 'year_10'), ('year_11', 'year_11'), ('year_12', 'year_12')], max_length=13)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'questions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_title', models.CharField(max_length=255)),
                ('quiz_level', models.CharField(default='year_1', max_length=50)),
                ('total_marks', models.IntegerField()),
                ('quiz_status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'quiz',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('fullName', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('parent', 'Parent'), ('student', 'Student'), ('teacher', 'Teacher')], max_length=50)),
                ('academicLevel', models.TextField()),
                ('userStatus', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='StudentExam',
            fields=[
                ('student_exam_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0)),
                ('taken_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.quiz')),
                ('student', models.ForeignKey(blank=True, limit_choices_to={'role': 'student'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
            options={
                'db_table': 'Student_Exams',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_answer', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.question')),
                ('student_exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.studentexam')),
            ],
            options={
                'db_table': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='AIAnalysis',
            fields=[
                ('analysis_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('Arithmetic', 'Arithmetic'), ('Trigonometry', 'Trigonometry'), ('Algebra', 'Algebra'), ('Geometry', 'Geometry'), ('Calculus', 'Calculus')], max_length=50)),
                ('score_percentage', models.FloatField(default=0.0)),
                ('improvement_tips', models.TextField(null=True)),
                ('student_exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.studentexam')),
            ],
            options={
                'db_table': 'AI_Analysis',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='teacher',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'teacher'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.user'),
        ),
        migrations.CreateModel(
            name='Doubt',
            fields=[
                ('doubt_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Answered', 'Answered')], default='Pending', max_length=10)),
                ('ai_response', models.TextField(blank=True, null=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(blank=True, limit_choices_to={'role': 'student'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
            options={
                'db_table': 'Doubts',
            },
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=1)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.question')),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.quiz')),
            ],
            options={
                'db_table': 'quiz_questions',
                'unique_together': {('quiz', 'question')},
            },
        ),
        migrations.CreateModel(
            name='ParentStudentMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(blank=True, limit_choices_to={'role': 'parent'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_links', to='myapp.user')),
                ('student', models.ForeignKey(blank=True, limit_choices_to={'role': 'student'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_links', to='myapp.user')),
            ],
            options={
                'db_table': 'Parent_Student_Mapping',
                'unique_together': {('parent', 'student')},
            },
        ),
    ]

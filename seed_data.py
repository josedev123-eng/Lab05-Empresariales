import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'admin123'
os.environ['DJANGO_SUPERUSER_USERNAME'] = 'admin'
os.environ['DJANGO_SUPERUSER_EMAIL'] = 'admin@example.com'

import django
django.setup()

from quiz.models import Exam, Question, Choice

# Create exam
exam = Exam.objects.create(
    title="Sample Exam",
    description="This is a sample exam for demonstration"
)

# Create first question
q1 = Question.objects.create(
    exam=exam,
    statement="What is Python?"
)

# Create choices for q1 (exactly one correct)
Choice.objects.create(question=q1, text="A snake", is_correct=False)
Choice.objects.create(question=q1, text="A programming language", is_correct=True)
Choice.objects.create(question=q1, text="A snake charmer", is_correct=False)
Choice.objects.create(question=q1, text="A type of data", is_correct=False)

# Create second question
q2 = Question.objects.create(
    exam=exam,
    statement="Which keyword creates a function?"
)

# Create choices for q2 (exactly one correct)
Choice.objects.create(question=q2, text="def", is_correct=True)
Choice.objects.create(question=q2, text="function", is_correct=False)
Choice.objects.create(question=q2, text="import", is_correct=False)
Choice.objects.create(question=q2, text="class", is_correct=False)

print("Exam and questions/choices seeded successfully!")
print(f"Exam: {exam}")
print(f"Questions: {exam.questions.count()}")
for q in exam.questions.all():
    print(f"  - {q}: {q.choices.count()} choices")
    correct = q.choices.filter(is_correct=True).count()
    print(f"    Correct choices: {correct}")
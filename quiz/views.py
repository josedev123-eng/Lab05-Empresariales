from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceForm, ChoiceFormSet


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "quiz/exam_list.html", {"exams": exams})


def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, "quiz/exam_detail.html", {"exam": exam})


def question_create(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if request.method == "POST":
        q_form = QuestionForm(request.POST)
        c_formset = ChoiceFormSet(request.POST)
        if q_form.is_valid() and c_formset.is_valid():
            # Enforce exactly one correct choice
            correct_count = sum(
                1 for form in c_formset if form.cleaned_data.get("is_correct")
            )
            if correct_count != 1:
                # Add error to formset so user knows
                q_form.add_error(None, "Exactly one choice must be marked as correct.")
            else:
                question = q_form.save(commit=False)
                question.exam = exam
                question.save()
                for form in c_formset:
                    choice = form.save(commit=False)
                    choice.question = question
                    choice.save()
                return redirect("quiz:exam_detail", pk=exam.pk)
    else:
        q_form = QuestionForm()
        c_formset = ChoiceFormSet()
    return render(
        request,
        "quiz/question_form.html",
        {"exam": exam, "q_form": q_form, "c_formset": c_formset},
    )
from django import forms
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["title", "description"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["statement"]


ChoiceFormSet = forms.modelformset_factory(
    Choice,
    fields=["text", "is_correct"],
    extra=4,
    max_num=4,
    validate_max=True,
)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text", "is_correct"]

    def clean(self):
        cleaned_data = super().clean()
        is_correct = cleaned_data.get("is_correct")
        # We'll enforce exactly one correct at the formset level
        return cleaned_data
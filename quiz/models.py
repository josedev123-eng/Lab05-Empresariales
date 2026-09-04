from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creation_date"]
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    statement = models.TextField()
    score = models.IntegerField(default=0, help_text="Points awarded for a correct answer")

    class Meta:
        ordering = ["id"]
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.exam.title} – {self.statement[:30]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return f"{self.question.statement[:20]} – {self.text}"

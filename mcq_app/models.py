from django.db import models

# Create your models here.
from django.db import models


CORRECT_ANSWER_CHOICES = [
    ('choice_a' ,'A'),
    ('choice_b' ,'B'),
    ('choice_c' ,'C'),
    ('choice_d' ,'D'),
]
class MCQQuestion(models.Model):
    
    question_text = models.TextField(verbose_name="Question")
    
    choice_a = models.CharField(max_length=255, verbose_name="Choice A")
    choice_b = models.CharField(max_length=255, verbose_name="Choice B")
    choice_c = models.CharField(max_length=255, verbose_name="Choice C")
    choice_d = models.CharField(max_length=255, verbose_name="Choice D")
    
    correct_answer = models.CharField(
        max_length=10, 
        choices=CORRECT_ANSWER_CHOICES,
        help_text="Select the correct option"
    )

    def __str__(self):
        return self.question_text[:50]
    
class Result(models.Model):
    stu_id = models.CharField(max_length=20)
    score = models.IntegerField()

    def __str__(self) -> str:
        return self.stu_id
from django.shortcuts import render
from .models import MCQQuestion

def mcq_list(request):
    questions = MCQQuestion.objects.all()

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()

        for question in questions:
            
            post_key = f"question_{question.id}"
            
            user_answer = request.POST.get(post_key)

            # Compare user input with the correct database answer
            if user_answer == question.correct_answer:
                score += 1
        return render(request, 'mcq_questions.html', {
            'score': score,
            'total': total_questions
        })

    return render(request, 'mcq_questions.html', {'questions': questions})
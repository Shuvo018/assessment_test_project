from django.shortcuts import render
from .models import MCQQuestion, Result
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mcq_list(request):
    questions = MCQQuestion.objects.all()

    if request.method == 'POST':
        score = 0
        user_id = request.POST.get('user_id')
        total_questions = questions.count()

        for question in questions:
             
            post_key = f"question_{question.id}"
            
            user_answer = request.POST.get(post_key)

            # Compare user input with the correct database answer
            if user_answer == question.correct_answer:
                score += 1
        
        try:
            Result.objects.create(stu_id= user_id, score=score)
            print('result added')
        except Exception as e:
            print(e)

        return render(request, 'mcq_questions.html', {
            'score': score,
            'total': total_questions
        })

    return render(request, 'mcq_questions.html', {'questions': questions})
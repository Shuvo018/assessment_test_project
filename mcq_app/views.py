from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import get_questions
from .models import MCQQuestion
from .tasks import score_and_save


@csrf_exempt
def mcq_list(request):
    questions = get_questions()
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        answers = {f"question_{q.id}": request.POST.get(f"question_{q.id}") for q in questions}
        score_and_save.delay(user_id, answers)
        return redirect('submit')
    return render(request, "mcq_questions.html", {"questions": questions})

def submit(request):
    return render(request, 'submit.html')
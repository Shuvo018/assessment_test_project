from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import MCQQuestion
from .tasks import save_result_to_cache


@csrf_exempt
def mcq_list(request):

    questions = MCQQuestion.objects.all()

    if request.method == "POST":

        score = 0

        user_id = request.POST.get(
            "user_id"
        )

        for question in questions:

            post_key = (
                f"question_{question.id}"
            )

            user_answer = request.POST.get(
                post_key
            )

            if (
                user_answer
                == question.correct_answer
            ):
                score += 1

        # Send to Redis Queue
        save_result_to_cache.delay(
            user_id,
            score
        )

        return render(
            request,
            "mcq_questions.html"
        )

    return render(
        request,
        "mcq_questions.html",
        {"questions": questions}
    )
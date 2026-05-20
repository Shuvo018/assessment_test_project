# utils.py

from django.core.cache import cache
from .models import MCQQuestion


def get_questions():

    cache_key = "mcq_questions"
    cache.delete(cache_key)
    questions = cache.get(cache_key)

    if questions is None:

        questions = list(MCQQuestion.objects.all())

        cache.set(
            cache_key,
            questions,
            timeout=3600 # 1 hour
        )

        print("Fetched from DB")

    else:
        print("Fetched from Redis")

    return questions
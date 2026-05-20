# mcq/tasks.py
from celery import shared_task
from django.core.cache import cache


@shared_task
def save_result_to_cache(stu_id, score):

    redis_key = "mcq_results"

    existing_results = cache.get(redis_key, [])

    existing_results.append({
        "stu_id": stu_id,
        "score": score
    })

    cache.set(redis_key, existing_results)
    
    return "Added to Redis"


from .models import Result


@shared_task
def bulk_insert_results():

    redis_key = "mcq_results"

    cached_results = cache.get(
        redis_key,
        []
    )

    if not cached_results:
        return "No data"

    students = [
        Result(
            stu_id=item["stu_id"],
            score=item["score"]
        )
        for item in cached_results
    ]

    Result.objects.bulk_create(
        students,
        batch_size=100
    )

    cache.delete(redis_key)

    return (
        f"{len(students)} inserted"
    )
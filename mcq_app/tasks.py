# mcq/tasks.py
from celery import shared_task
from django.core.cache import cache
from django_redis import get_redis_connection


from .utils import get_questions

@shared_task
def score_and_save(stu_id, answers: dict):
    questions = get_questions()  # served from Redis, not DB
    
    score = sum(
        1 for q in questions
        if answers.get(f"question_{q.id}") == q.correct_answer
    )
    print(f"{stu_id}:{score}")
    redis = get_redis_connection("default")
    redis.rpush("mcq_results", f"{stu_id}:{score}")

from .models import Result

@shared_task
def bulk_insert_results():
    redis = get_redis_connection("default")
    
    raw = redis.lrange("mcq_results", 0, -1)
    if not raw:
        return "No data"
    redis.delete("mcq_results")  # delete BEFORE insert to avoid double-processing
    
    students = []
    for item in raw:
        stu_id, score = item.decode().split(":")
        students.append(Result(stu_id=stu_id, score=int(score)))
    
    Result.objects.bulk_create(students, batch_size=200)
    return f"{len(students)} inserted"
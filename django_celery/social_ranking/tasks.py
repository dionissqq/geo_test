from django.db.models import Sum
from celery import shared_task

from .models import Rank


# tasks' interfaces
@shared_task(name='check_score_out_of_range')
def check_score_out_of_range(user_id, score):
    pass

@shared_task(name='check_overall_score_out_of_range')
def check_overall_score_out_of_range(score):
    pass


# repeated_task
@shared_task
def check_all_ranks_sum():
    sum = Rank.objects.aggregate(Sum('score')) 
    sum = sum['score__sum']
    if sum:
        check_overall_score_out_of_range.delay(sum)
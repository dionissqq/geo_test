from clickhouse_driver import Client
from celery import Celery
import logging

app = Celery('app', broker='redis://localhost:6379/0')

db_client = Client(host='localhost', password = 'pass')

db_client.execute('CREATE DATABASE IF NOT EXISTS rankings')
db_client.execute('DROP TABLE IF EXISTS rankings.score')
db_client.execute('CREATE TABLE IF NOT EXISTS rankings.score (x Int32) ENGINE = MergeTree() ORDER BY tuple()')


@app.task
def send_notification(message):
    logging.info(message)

@app.task(name='check_score_out_of_range')
def check_score_out_of_range(user_id, score):
    if score==0 or score >1000:
        send_notification.delay(
            'user {0} now has balance of {1} points'.format(user_id,score)
        )

@app.task(name='check_overall_score_out_of_range')
def check_overall_score_out_of_range(score):
    db_client.execute(
        'INSERT INTO rankings.score (x) VALUES ({0})'.format(score)
    )
    if score >100000:
        send_notification.delay(
            'averallscore now is {0}'.format(score)
        )


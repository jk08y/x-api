from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    return scheduler

def schedule_post(scheduler, client, tweet_content, post_time):
    post_time = datetime.strptime(post_time, '%Y-%m-%d %H:%M:%S')
    scheduler.add_job(
        func=lambda: client.create_tweet(text=tweet_content),
        trigger='date',
        run_date=post_time,
        id=str(post_time.timestamp())
    )

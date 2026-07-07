from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from datetime import datetime
from uuid import uuid4

def init_scheduler():
    """Initialize and start the BackgroundScheduler."""
    scheduler = BackgroundScheduler()
    scheduler.start()
    return scheduler

def schedule_post(scheduler, client, tweet_content, post_time):
    """
    Schedule a post to be published at a specific time.

    Args:
        scheduler: Instance of BackgroundScheduler.
        client: API client with a `create_tweet` method.
        tweet_content: The content of the tweet.
        post_time: Scheduled time as a string in '%Y-%m-%d %H:%M:%S' format.

    Raises:
        ValueError: If `post_time` cannot be parsed.
        JobLookupError: If a job with the same ID already exists.
    """
    try:
        # HTML datetime-local fields submit "YYYY-MM-DDTHH:MM".
        normalized_time = post_time.replace("T", " ")
        try:
            post_time_dt = datetime.strptime(normalized_time, '%Y-%m-%d %H:%M')
        except ValueError:
            post_time_dt = datetime.strptime(normalized_time, '%Y-%m-%d %H:%M:%S')
        
        # Generate a unique job ID based on post time
        job_id = f"tweet_{post_time_dt.timestamp()}_{uuid4().hex[:8]}"
        
        # Add the job to the scheduler
        scheduler.add_job(
            func=lambda: client.create_tweet(text=tweet_content),
            trigger='date',
            run_date=post_time_dt,
            id=job_id
        )
        print(f"Scheduled post '{tweet_content}' for {post_time}.")
    except ValueError as ve:
        print(f"Error: Invalid date format for post_time '{post_time}'. Use 'YYYY-MM-DD HH:MM:SS'.")
        raise ve
    except JobLookupError as jle:
        print(f"Error: A job with ID '{job_id}' already exists.")
        raise jle
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e

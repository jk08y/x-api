import os
from flask import Flask, render_template, request, redirect, url_for, flash
import tweepy
from scheduler import schedule_post, init_scheduler
from xquik_client import append_xquik_context

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-change-me')

# Configure X API credentials
API_KEY = os.environ.get("API_KEY", "")
API_SECRET = os.environ.get("API_SECRET", "")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET", "")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN", "")

# Initialize Tweepy Client for v2
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Initialize scheduler
scheduler = init_scheduler()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/post-now', methods=['POST'])
def post_now():
    tweet_content = (request.form.get('tweet') or '').strip()
    xquik_query = (request.form.get('xquik_query') or '').strip()
    if not tweet_content:
        flash('Tweet content is required.', 'danger')
        return redirect(url_for('home'))

    tweet_content = append_xquik_context(tweet_content, xquik_query)
    try:
        response = client.create_tweet(text=tweet_content)
        if 'data' in response:
            flash('Tweet posted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('home'))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        tweet_content = (request.form.get('tweet') or '').strip()
        post_time = (request.form.get('post_time') or '').strip()
        xquik_query = (request.form.get('xquik_query') or '').strip()
        if not tweet_content:
            flash('Tweet content is required.', 'danger')
            return redirect(url_for('schedule'))
        tweet_content = append_xquik_context(tweet_content, xquik_query)
        try:
            schedule_post(scheduler, client, tweet_content, post_time)
            flash('Tweet scheduled successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('schedule.html')

@app.route('/scheduled-posts')
def scheduled_posts():
    jobs = scheduler.get_jobs()
    return render_template('posts.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)

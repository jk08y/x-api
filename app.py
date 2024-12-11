from flask import Flask, render_template, request, redirect, url_for, flash
import tweepy
from scheduler import schedule_post, init_scheduler

app = Flask(__name__)
app.secret_key = ''

# Configure X API credentials
API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""
BEARER_TOKEN = ""

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
    tweet_content = request.form.get('tweet')
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
        tweet_content = request.form.get('tweet')
        post_time = request.form.get('post_time')
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

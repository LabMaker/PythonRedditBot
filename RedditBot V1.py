import praw
import re
import time
from prawcore import PrawcoreException

reddit = praw.Reddit(client_id='clientId', 
            client_secret='clientSecret',
            user_agent='<platform:FireFox:0.0.1 (by //',
            username='username',
            password='password')


reddit.validate_on_submit = True


title = "hello",
titleBody = "Please Contact me on reddit and i will be able to help you"

subreddits = ['subreddit1', 'subreddit2']

print(reddit.read_only)

pos = 0


def post():
    global subreddits
    global pos
    
    try:
        subreddit = reddit.subreddit(subreddits[pos])
        subreddit.submit(title, titleBody)
        pos = pos + 1

        if (pos <= len(subreddits) - 1):
            post()
        else:
            print("Sleeping for 6 hours")
            Time.Sleep(21600)
            pos = 0
            post()
    except praw.exceptions.RedditAPIException as e:
        print(e.items[0].message)
        if (e.items[0].error_type == "RATELIMIT"):
            delay = re.search("(\d+) minutes", e.items[0].message)

            if delay:
                delay_seconds = float(int(delay.group(1)) * 60)
                print("Sleeping for " + str(delay_seconds))
                time.sleep(delay_seconds)
                post()
            else:
                delay = re.search("(\d+) seconds", e.items[0].message)
                delay_seconds = float(int(delay.group(1)))
                print("Sleeping for " + str(delay_seconds))
                time.sleep(delay_seconds)
                post()




post()
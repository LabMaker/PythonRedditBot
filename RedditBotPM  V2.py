import praw
import re
import time
import json
from prawcore import PrawcoreException
import os


reddit = praw.Reddit(client_id='clientId', 
            client_secret='clientSecret',
            user_agent='<platform:Firefox:0.0.1 (by //',
            username='username',
            password='password') 


reddit.validate_on_submit = True

config = ""
with open('config.json') as config_file:
    config = json.load(config_file)
    

pos = 0

subreddits =  config['subreddits']
title = config['title']
pmBody = config['pmBody']
forbiddenWords = config['forbiddenWords']

submission_IDs = []

fileObj = open("submissionids.txt", "r") #opens the file in read mode
submission_IDs = fileObj.read().splitlines() #puts the file into an array
fileObj.close()



counter = 0
print("Started Bot...")
print(type(subreddits))

def post():
    global subreddits
    global pos
    global counter
    try:
        subreddit = reddit.subreddit(subreddits[pos])
        for submission in subreddit.new(limit=10):
            if (submission.id not in submission_IDs):
                print(f"{counter}:{subreddit.display_name}")
                counter = counter + 1
                #print("Checking Submission")
                isValid = True
                for word in forbiddenWords:
                    if (word in submission.title.lower() or word in submission.selftext.lower()):
                        isValid = False
                
                if (isValid):
                    print(f"{counter}:{submission.author}:{subreddit.display_name}")
                    submission.author.message(title, pmBody)
                    
                submission_IDs.append(submission.id)
                SaveTextFile()
                time.sleep(30)
            #else:
                #print("Already Checked Submission") #Commented As it comments this 50x when restarting program
        pos = pos + 1
        if (pos <= len(subreddits) - 1):
            post()
        else:
            pos = 0
            print(f"{counter}:NextReddit")
            time.sleep(120) #Sleep For 2 Minutes before re checking for new posts
            post()
    except praw.exceptions.RedditAPIException as e:
        print(e.items[0].message)
        print(e.items[0].error_type)
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
        if (e.items[0].error_type == "NOT_WHITELISTED_BY_USER_MESSAGE"):
            print("Blocked By user Skipping Submission")
            submission_IDs.append(submission.id)
            SaveTextFile()
            post()



def SaveTextFile():
    with open("submissionids.txt", "w") as o:
        for line in submission_IDs:
            print(line, file=o)


while (True):
    try:
        post()
    except Exception as e:
        print("Error In Main: " + e)
    finally:
        post()

# PythonRedditBot
 
This was the original bot which was a single file app which would store data locally into a file.

This project is not to be used and is only a showcase of the code which was turned into what LabMaker is today.


## V1
Version One Was Created at the start of february and was a basic bot which had the user manually input details for the subreddits and login details. 
No data was stored or saved and it would essentially just create a post on each subreddit advertising for users to contact you.

## V2
After a few days of using V1 the issue with re-pming people and checking over posts it had already done was becoming an issue so i first created a bot which comments on each post however their was a ratelimit
issue where too many posts where getting checked so i wasnt able to comment on them all. Instead i changed it to a PM bot which has no issue with ratelimiting. The program was terribly coded and did not handle
exceptions properly i had to an extra program to check if the process closed to automatically reopen it. 
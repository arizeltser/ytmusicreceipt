# ytmusicreceipt
A take on Receiptify (https://receiptify.herokuapp.com/index.html).

Every month an email is sent containing the users ten most listened to songs from Youtube Music.

Songs are determined by retrieval of Youtube Music history using ytmusicapi (https://ytmusicapi.readthedocs.io/en/stable/index.html)

Script is run as a github action according to cron scheduling.

Created as a fun side project to explore API calls, containerization, and job scheduling.
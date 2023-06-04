from ytmusicapi import YTMusic
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os

# setup connection to YTMusic
try:
    OAUTH = os.environ["OAUTH_SECRET"]
except KeyError:
    raise KeyError("OAUTH_SECRET not available!")

ytmusic = YTMusic(OAUTH)

# get current date
current_date = datetime.datetime.now()
year = current_date.year

# get previous month
previous_month = current_date.month - 1
if previous_month == 0:
    previous_month = 12
    year = current_date.year - 1
previous_month_name = datetime.date(1900, previous_month, 1).strftime('%B')
year_name = str(year)

if current_date.day == 4:
    # get history
    history = ytmusic.get_history()

    # list of ok results of played variable
    ok_played = ['Today','Yesterday','Last week',previous_month_name+' '+year_name]

    times_played = {}
    for item in history:
        if item['played'] in ok_played:
            if item['title'] in times_played:
                times_played[item['title']] += 1
            else:
                times_played[item['title']] = 1

    # sort by most played
    sorted_times_played = sorted(times_played.items(), key=lambda x: x[1], reverse=True)

    # print results
    message = ''
    print('Top 10 songs played in ' + previous_month_name + ' ' + year_name)
    for i in range(10):
        if sorted_times_played[i][1] <= 1:
            message = message + 'No more songs played more than once' + '\n'
            print('No more songs played more than once')
            break
        message = message + str(i+1) + '. ' + sorted_times_played[i][0] + ' - ' + str(sorted_times_played[i][1]) + ' times' + '\n'
        print(str(i+1) + '. ' + sorted_times_played[i][0] + ' - ' + str(sorted_times_played[i][1]) + ' times')


smtp_server = "smtp.gmail.com" 
smtp_port = 587

emailauth_file = os.getenv("EMAILAUTH_JSON")
try:
    EMAILAUTH = os.environ["EMAILAUTH_SECRET"]
except KeyError:
    raise KeyError("EMAILAUTH_SECRET not available!")
emailAuth = json.loads(EMAILAUTH)

login_email = emailAuth['email']
login_password = emailAuth['password']

msg = MIMEMultipart()
msg["From"] = login_email
msg["To"] = 'ari.zeltser@gmail.com'
msg["Subject"] = 'Top 10 songs played in ' + previous_month_name + ' ' + year_name

body = message
msg.attach(MIMEText(body, "plain"))

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(login_email, login_password)
    server.send_message(msg)


           
    








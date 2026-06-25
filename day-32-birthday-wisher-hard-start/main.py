import smtplib
import pandas
import datetime as dt
import random
import os
from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")

data = pandas.read_csv('birthdays.csv')
birthdays_dict = data.to_dict(orient='records')
now = dt.datetime.now()

def send_bday_email(friend):
    if (now.month, now.day) == (friend['month'], friend['day']):
        with open(f'letter_templates/letter_{random.randint(1, 3)}.txt', 'r') as letter_file:
            letter_content = letter_file.read()
            new_letter = letter_content.replace('[NAME]', friend['name'])
    
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=friend['email'],
                msg=f'Subject: Happy Birthday!\n\n{new_letter}'
            )

for friend in birthdays_dict:
    send_bday_email(friend)
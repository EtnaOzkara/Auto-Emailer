import smtplib
import pandas as pd


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#read data from csv file
data = pd.read_csv(r'FILEPATH TO CSV')
#create a new column to track the emails
data["Status"] = "not sent"
data.to_csv(r'FILEPATH TO CSV', index=False)

#append the data into an array
names = []
emails = []
statuss = []


for name in data.Name:
    names.append(name)

for email in data.Email:
    emails.append(email)

for status in data.Status:
    statuss.append(status)

#method to check if the data is empty
def isNaN(string):
    return string != string

me='SALES PERSON EMAIL'

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login(me, 'ADD APP PASSWORD')

sales_name="SALES PERSON NAME"

for i in range(len(emails)):
    my_email = emails[i]
    my_name= names[i]
    #check if there is a name and email, dont send if there isnt
    if  isNaN(my_name)  or  isNaN(my_email):
        statuss[i]="no name or no email"

    #Try to send the email
    else:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "{my_name}, Research Inquiry".format(my_name=my_name.split()[0])
            msg['From'] = me
            msg['To'] = my_email

            html = """\
            <html>
              <head></head>
              <body>
                <p>Dear {my_name},</p>

                <p>My name is {sales_name}, I'm a <b>StudyFind</b> representative, our <b>organization</b> and <b>software</b> are oriented around aiding in the <b>communication and coordination</b> between <i>researchers</i> and <i>participants</i> of research studies. Our goal is to minimize all the mundane tasks of running a study. Such as:<br>
                &emsp; &bull; Pre-screening<br>
                &emsp; &bull; Messaging<br>
                &emsp; &bull; Setting Meetings <br>
                &emsp; &bull; Reminders, etc. <br>
                <br>
                We have streamlined these features onto one platform that <i>researchers</i> can utilize for multiple studies simultaneously.</p>

                <p>I was hoping you had time this week or next week to get on a call to speak about potentially utilizing the <b>StudyFind</b> software for your future research? also, if you have any questions please don't hesitate to follow up with me here. <br>
                <br>

                <p>Let me know if you're interested! Speak to you soon and have a great day!<br><br>
                Sincerely, <br>
                {sales_name}<br><br>
                StudyFind | Technical Sales | 423 E Clement St, Baltimore, MD</p>
                <br><br>
                <p>P.S. If you have 30 seconds to spare I have linked our recently completed animated commercial for your viewing pleasure.</p> <br>

                 <a href="https://youtu.be/5_iZ0r33wWk">  <center> <img src="https://i.giphy.com/media/hUmjETCYIYRBZRPwTg/giphy.gif" width="40%" alt="StudyFind"> </img> </center> </a>
              </body>
            </html>
            """.format(my_name=my_name.split()[0], sales_name=sales_name)

            part1 = MIMEText(html, 'html')

            msg.attach(part1)

            mail.sendmail(me, my_email, msg.as_string())

            statuss[i]="sent"
        #if cannot send, move on
        except Exception as e:
            print(e)
            statuss[i]="cannot be sent"
            print("moving on")

#update the status column in the csv file
data["Status"] = statuss
data.to_csv(r'/FILEPATH TO CSV', index=False)

#close server
mail.quit()

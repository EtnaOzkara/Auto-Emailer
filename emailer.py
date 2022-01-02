import smtplib
import pandas as pd

#read data from csv file
data = pd.read_csv(r'/Users/etnaozkara/Desktop/emailer/Emails.csv')
#create a new column to track the emails
data["Status"] = "not sent"
data.to_csv(r'/Users/etnaozkara/Desktop/emailer/Emails.csv', index=False)

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

#Email of the sender
FROMADDR = "INPUT YOUR EMAIL"
LOGIN    = FROMADDR
#Password of the sender
PASSWORD = "INPUT PASSWORD (COULD USE AN APP PASSWORD FOR SAFETY)"
server = smtplib.SMTP('smtp.gmail.com', 587)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(LOGIN, PASSWORD)

for i in range(len(emails)):
    my_email = emails[i]
    my_name= names[i]
    #check if there is a name and email, dont send if there isnt
    if  isNaN(my_name)  or  isNaN(my_email):
        statuss[i]="no name or no email"

    #Try to send the email
    else:
        try:
            #Subject
            SUBJECT  = "Test Email"
            TOADDRS  = my_email
            msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
                % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
            #Message goes here
            msg += "Hello {},\n Hope you had a wonderful day! \n \n Sincerely, \n Etna Ozkara".format(my_name)
            server.sendmail(FROMADDR, TOADDRS, msg)
            #update the status array to sent
            statuss[i]="sent"
        #if cannot send, move on
        except Exception as e:
            statuss[i]="cannot be sent"
            print("moving on")

#update the status column in the csv file
data["Status"] = statuss
data.to_csv(r'/Users/etnaozkara/Desktop/emailer/Emails.csv', index=False)

#close server
server.quit()

#*************************************************************************************************
#****************************** SENDING EMAIL*****************************************************
#*************************************************************************************************

import smtplib
import os
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


#variable name server, which will store the specific server we are going to use 
#Note: this is current setup is for gmail, you can find info about your email provider 
#      online. Browse for SMTP of the the email provider you use
server = smtplib.SMTP('smtp.gmail.com', 587)

EmailVar = 'elegproffesor@gmail.com'

server.ehlo()

#opening the file where the password for the senders email is stored
#and store it into a variable name password
with open("password.txt", "r") as f:
    password = f.read()


#Connecting to the gmail SMTP server 
#If you use a different email, look up the required SMTP server 
server.connect("smtp.gmail.com",587)
server.ehlo()
server.starttls()

#Login to the senders email
server.login('FRAT.seniordesign@gmail.com', password)


#Constructing a basic Heading for the email 
msg =MIMEMultipart()
msg['From'] = 'FRAT'
msg['To'] = 'elegproffesor@gmail.com'
msg['Subject'] = 'Attendance'

body = "Attendance list attached below"

msg.attach(MIMEText(body, "plain"))

filename = "Attendance.csv"  # In same directory as script

# Open CSV file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
msg.attach(part)
text = msg.as_string()



def send_Email():
    server.sendmail('FRAT.seniordesign@gmail.com', 'elegproffesor@gmail.com' , text)

    server.quit()

#************************************************************************************************************************

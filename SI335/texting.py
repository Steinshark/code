import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sms_gateway = '6129795468@vtext.com'
smtp = 'smtp.gmail.com'
port = 587

email = "everettperson@gmail.com"
server = smtplib.SMTP(smtp,port)
server.starttls()
server.login(email,"steinshark")



msg = MIMEMultipart()
msg['From'] = email
msg['To'] = sms_gateway
# Make sure you add a new line in the subject
msg['Subject'] = "You can insert anything\n"
# Make sure you also add new lines to your body
body = "You can insert message here\n"
# and then attach that body furthermore you can also send html content.
msg.attach(MIMEText(body, 'plain'))

sms = msg.as_string()

server.sendmail(email,sms_gateway,sms)

# lastly quit the server
server.quit()

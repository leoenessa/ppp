import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

gmail_user = 'leonardooc@globo.com'  
gmail_password = 'leoenessa'
'''
OUTRA TENTATIVA
'''
msg = MIMEMultipart()
msg['Subject'] = 'Assunto'
msg['From'] = 'leonardooc@globo.com'
msg['To'] = 'leonardooc@globo.com'
msg.preamble = "reuniao de familia"

part = MIMEBase("image","octet-stream")
part.set_payload(open('teste.jpg','rb').read())
encoders.encode_base64(part)

part.add_header('Content-Disposition', 'attachment; filename="teste.jpg"')
#============================
#sent_from = gmail_user  
#to = ['leonardooc@globo.com']  
#subject = 'OMG Super Important Message'  
#body = 'OK'

#img_data = open('teste.jpg', 'rb').read()
'''with open('teste.jpg','rb') as fp:
    img = MIMEImage(fp.read())'''

msg.attach(part)

#image = MIMEImage(img_data, name=os.path.basename('teste.jpg'))


try:  
    server = smtplib.SMTP_SSL('smtp.globo.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, gmail_user, msg.as_string())
    #server.send_message(msg)
    server.close()

    print('Email sent!')
except smtplib.SMTPException as e:  
    #print('Something went wrong...'+str(e))
    print(str(e))

'''  img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'subject'
    msg['From'] = 'e@mail.cc'
    msg['To'] = 'e@mail.cc'

    text = MIMEText("test")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP(Server, Port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(UserName, UserPassword)
    s.sendmail(From, To, msg.as_string())
    s.quit()'''

import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def sendEmailWithImg(fromAddress = "sebas.rivera96@gmail.com", toAddress = "sebastian.rivera@ipointsystems.com", fileName = "temp.jpg", pathToImg = "./temp.jpg"):     
    """
    Function Name:
        sendEmailWithImg
    Objective:
        Send an EMAIL using the TLS protocol and send an image.
    Input parameter(s):
        - fromAddress : a string indicating the sender address.
        - toAddress : a list of strings (or single string when just one) which indicates the receivers of the picture.
        - fileName : name of the image file
        - pathToImg : COMPLETE path indicating the exact location of the image file.
    Output parameter(s):
        * None
    """
    msg = MIMEMultipart()
    fromPassword = "Junio#261996"
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = "A picture from you!"
    
    body = "\nHi there,\n\ntabellarius found a picture from you. Enjoy it!\n\nKind Regards,\nIPS Family" 
    
    msg.attach(MIMEText(body, 'plain'))
    
    attachment = open(pathToImg, "rb")
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
    
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, fromPassword)
    text = msg.as_string()
    server.sendmail(fromAddress, toAddress, text)
    server.quit()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sendEmailWithImg()
    else:
        sendEmailWithImg(toAddress = sys.argv[1])
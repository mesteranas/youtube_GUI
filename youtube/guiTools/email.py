from plyer import email
def sendEmail(to,subject,message):
    email.send(recipient=to, subject=subject, text=message, create_chooser=False)
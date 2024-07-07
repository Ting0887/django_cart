from django.conf import settings
from django.core.mail import EmailMessage

def send_simple_message(mailto, mailsubject, mailcontent):
    email = EmailMessage(mailsubject,mailcontent,settings.EMAIL_HOST_USER,[mailto])
    email.fail_silently = False
    email.send()


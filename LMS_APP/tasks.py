# myapp/tasks.py
from background_task import background
from django.core.mail import send_mail
from django.conf import settings

@background(schedule=5)  # You can set the task to run after 60 seconds or any other interval
def send_email_background(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
    )

# myapp/tasks.py
from background_task import background
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@background(schedule=5)  # You can set the task to run after 60 seconds or any other interval
def send_email_background(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
    )

@background(schedule=5)
def send_password_reset_email(user_email, reset_url):
    subject = "Confirm Your Password Update Request"
    context = {
        'reset_url': reset_url
    }
    message = render_to_string('reset/update_password.html', context)
    email = EmailMessage(subject, message, to=[user_email])
    email.content_subtype = 'html'
    email.send()
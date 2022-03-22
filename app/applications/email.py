from django.core.mail import send_mail
from rest_framework.reverse import reverse
from users.tokens import account_activation_token
from skillactive.settings import HOST_VARIABLE
from django.template.loader import render_to_string


def send_application_email(application):
    mail_subject = f"Новая зявка на секцию {application.club.title} на skillactive.ru"
    message = f"{application.club.title}, {application.name}, {application.phone}, {application.text}"
    to_email = application.club.author.email
    html_page = render_to_string(
        "application.html",
        {
            "club_name": application.club.title,
            "name": application.name,
            "phone": application.phone,
            "text": application.text,
        },
    )
    send_mail(mail_subject, message, None, [to_email], html_message=html_page)

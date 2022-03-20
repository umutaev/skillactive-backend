from django.core.mail import send_mail
from rest_framework.reverse import reverse
from users.tokens import account_activation_token
from skillactive.settings import HOST_VARIABLE
from django.template.loader import render_to_string


def send_activation_email(user):
    mail_subject = "Регистрация на skillactive.ru"
    uid = str(user.pk)
    token = account_activation_token.make_token(user)
    message = HOST_VARIABLE[:-1] + reverse(
        "verify-account", kwargs={"uid": uid, "token": token}
    )
    to_email = user.email
    html_page = render_to_string(
        "mail.html",
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "uid": uid,
            "token": token,
        },
    )
    send_mail(mail_subject, message, None, [to_email], html_message=html_page)


def send_restore_mail(user):
    mail_subject = "Restore your account."
    uid = str(user.pk)
    token = account_activation_token.make_token(user)
    message = f"{uid} {token}"
    to_email = user.email
    html_page = render_to_string(
        "recover.html",
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "uid": uid,
            "token": token,
        },
    )
    send_mail(mail_subject, message, None, [to_email])

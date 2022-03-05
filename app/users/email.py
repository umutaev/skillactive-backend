from django.core.mail import send_mail
from rest_framework.reverse import reverse
from users.tokens import account_activation_token
from skillactive.settings import HOST_VARIABLE


def send_activation_email(user):
    mail_subject = "Activate your account."
    uid = str(user.pk)
    token = account_activation_token.make_token(user)
    message = HOST_VARIABLE[:-1] + reverse(
        "verify-account", kwargs={"uid": uid, "token": token}
    )
    to_email = user.email
    send_mail(mail_subject, message, None, [to_email])

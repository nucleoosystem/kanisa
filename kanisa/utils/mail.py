from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from kanisa import conf


def send_bulk_mail(users, subject, template, ctx):
    context = Context(ctx)
    template_root = 'kanisa/emails/'

    plaintext_email = get_template(template_root + template + ".txt")
    html_email = get_template(template_root + template + ".html")

    plaintext_content = plaintext_email.render(context)
    html_content = html_email.render(context)

    for u in users:
        msg = EmailMultiAlternatives(subject,
                                     plaintext_content,
                                     conf.KANISA_FROM_EMAIL,
                                     [u.email, ])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_single_mail(user, subject, template, context):
    send_bulk_mail([user, ], subject, template, context)

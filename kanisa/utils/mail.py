from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from kanisa import conf


def send_mail_with_context(email, context, template):
    template_root = 'kanisa/emails/' + template

    subject = render_to_string(template_root + ".subj",
                               context).strip()
    plaintext = render_to_string(template_root + ".txt",
                                 context)
    html = render_to_string(template_root + ".html",
                            context)

    msg = EmailMultiAlternatives(
        subject,
        plaintext,
        conf.KANISA_FROM_EMAIL,
        [email, ]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()


def send_bulk_mail(users, template, context):
    context.update({'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME})

    for user in users:
        user_context = context.copy()
        user_context['addressee'] = user
        send_mail_with_context(user.email, user_context, template)


def send_single_mail(user, template, context):
    send_bulk_mail([user, ], template, context)

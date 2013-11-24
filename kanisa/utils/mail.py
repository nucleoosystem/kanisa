from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from kanisa import conf


def send_bulk_mail(users, template, context):
    context.update({'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME})

    template_root = 'kanisa/emails/' + template

    for u in users:
        user_context = context.copy()
        user_context['addressee'] = u
        subject = render_to_string(template_root + ".subj",
                                   user_context).strip()
        plaintext = render_to_string(template_root + ".txt",
                                     user_context)
        html = render_to_string(template_root + ".html",
                                user_context)

        msg = EmailMultiAlternatives(subject,
                                     plaintext,
                                     conf.KANISA_FROM_EMAIL,
                                     [u.email, ])
        msg.attach_alternative(html, "text/html")
        msg.send()


def send_single_mail(user, template, context):
    send_bulk_mail([user, ], template, context)

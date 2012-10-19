from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from kanisa import conf


def send_bulk_mail(users, template, ctx):
    ctx.update({'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME})

    context = Context(ctx)
    template_root = 'kanisa/emails/' + template

    subject_tmpl = get_template(template_root + ".subj")
    plaintext_tmpl = get_template(template_root + ".txt")
    html_tmpl = get_template(template_root + ".html")

    subject = subject_tmpl.render(context).strip()
    plaintext = plaintext_tmpl.render(context)
    html = html_tmpl.render(context)

    for u in users:
        msg = EmailMultiAlternatives(subject,
                                     plaintext,
                                     conf.KANISA_FROM_EMAIL,
                                     [u.email, ])
        msg.attach_alternative(html, "text/html")
        msg.send()


def send_single_mail(user, template, context):
    send_bulk_mail([user, ], template, context)

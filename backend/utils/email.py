from django.core.mail import send_mass_mail


def send_announcement_email(announcement, recipient_emails):
    subject = announcement.title
    message = announcement.message
    from_email = "sam.kipnis@gmail.com"

    email_data = [(subject, message, from_email, [email]) for email in recipient_emails]
    print(email_data)
    return send_mass_mail(email_data, fail_silently=False)

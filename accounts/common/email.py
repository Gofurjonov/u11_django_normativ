from django.core.mail import send_mail


def send_simple_email():
    send_mail(
        subject="Django email sinovi",
        message="Bu test email.",
        from_email="gafurjonovdavronbek@gmail.com",
        recipient_list=["a39307503@gmail.com", "freddyfazber040@gmail.com",
                        "akmalovabu96@gmail.com", "av3066827@gmail.com"],
        fail_silently=False,
    )

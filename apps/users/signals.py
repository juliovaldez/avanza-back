from django.dispatch import Signal,receiver
from apps.users.tasks import send_reset_email,send_activate_account

send_reset_email_signal = Signal()
send_activate_account_signal = Signal()

@receiver(send_reset_email_signal)
def send_reset_email_receiver(sender,user_id: int,**kwargs):
    send_reset_email.delay(user_id)



from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.inventory.models import Transaction



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print(f"Sender: {sender}")
    print(f"Instance: {instance}")
    print(f"Created: {created}")
    print(f"Additional kwargs: {kwargs}")

        

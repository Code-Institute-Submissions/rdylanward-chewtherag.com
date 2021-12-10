from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class AccountProfile(models.Model):
    """ An account profile model for maintaining default
        delivery information and order history """
    
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.account.accountname


@receiver(post_save, sender=User)
def create_or_update_account_profile(sender, instance, created, **kwargs):
    """ Create or update the account profile """
    
    if created:
        AccountProfile.objects.create(account=instance)
    # Existing account: just save the profile
    instance.accountprofile.save()
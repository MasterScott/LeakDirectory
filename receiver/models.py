from django.db import models

class Receiver(models.Model):
    id = models.CharField()
    name = models.CharField()
    description = models.CharField()
    pgp_key = models.CharField()
    oauth_token = models.CharField()


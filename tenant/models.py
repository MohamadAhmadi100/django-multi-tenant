import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class Organization(models.Model):
    name = models.CharField(max_length=100)
    auth0_Organization_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, related_name='users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    logged_in = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'({self.organization.name}) - {self.username}'

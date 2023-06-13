import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    auth0_tenant_id = models.CharField(max_length=100, unique=True)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, related_name='users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'({self.tenant.name}) - {self.username}'


class TenantRelatedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey('accounts.Tenant', related_name='%(class)s', on_delete=models.PROTECT, editable=False)

    class Meta:
        abstract = True

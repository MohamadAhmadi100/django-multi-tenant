import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class TenantManager(models.Manager):

    @transaction.atomic
    def create_account(self, tenant_name, username, password, tenant_address=None):
        tenant = Tenant(
            name=tenant_name,
            address=tenant_address,
        )
        tenant.save()

        user = User.objects.create_user(
            tenant=tenant,
            username=username,
            password=password,
        )

        return tenant, user

    @transaction.atomic
    def create_superuser(self, tenant, username, password, tenant_address=None):
        if None in [tenant, username, password]:
            raise TypeError('Superusers must have a password.')

        tenant, user = self.create_account(tenant, username, password, tenant_address)
        tenant.id = uuid.uuid4()
        tenant.is_superuser = True
        tenant.is_staff = True
        user.is_superuser = True
        user.is_staff = True
        tenant.id = uuid.uuid4()
        user.save()
        tenant.save()

        return tenant, user


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length=100, unique=True)
    address = models.CharField('address', max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TenantManager()

    class Meta:
        db_table = 'tenants'

    def __str__(self):
        return self.name


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

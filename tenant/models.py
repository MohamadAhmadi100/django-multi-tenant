from django.db import models
from main.config import setting


setting.get_cached_configs()


class Organization(models.Model):
    name = models.CharField(max_length=50, default="sponix-user")
    organization_id = models.CharField(max_length=100, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.set_organization_id()

    def set_organization_id(self):
        return self.organization_id

    @property
    def is_manager(self):
        if self.organization_id == setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY:
            return True
        return False


class MainUser(models.Model):
    user_id = models.CharField(unique=True, primary_key=True)
    organization = models.ForeignKey(Organization, related_name='users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['user_id', 'organization_id']

    def __str__(self):
        return f"userID: {self.user_id} organization: {self.organization_id}"

    @property
    def is_authenticated(self):
        if self.organization_id and self.user_id:
            return True
        return False

    @property
    def is_anonymous(self):
        if not self.organization_id or not self.user_id:
            return True
        return False

    @property
    def is_staff(self):
        if self.organization_id == setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY:
            return True
        return False

import pytest
from django.db import models
from main.config import setting
from tenant.models import Organization, MainUser

setting.get_cached_configs()


@pytest.fixture
def organization():
    return Organization.objects.create(
        name="sponix-user",
        organization_id=setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY
    )


@pytest.fixture
def main_user(organization):
    return MainUser.objects.create(
        user_id="test_user",
        organization=organization,
        active=True
    )


@pytest.mark.django_db
def test_organization_model(organization):
    assert organization.name == "sponix-user"
    assert organization.organization_id == setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY
    assert organization.set_organization_id() == organization.organization_id
    assert organization.is_manager is True


@pytest.mark.django_db
def test_main_user_model(main_user):
    assert main_user.user_id == "test_user"
    assert main_user.organization.name == "sponix-user"
    assert main_user.active is True
    assert str(main_user) == f"userID: {main_user.user_id} organization: {main_user.organization_id}"
    assert main_user.is_authenticated is True
    assert main_user.is_anonymous is False
    assert main_user.is_staff is True
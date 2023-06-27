import factory
from tenant.models import Organization, MainUser


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    organization_id = factory.Sequence(lambda n: f"org_{n}")
    name = "Test Organization"


class MainUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MainUser

    user_id = factory.Sequence(lambda n: f"user_{n}")
    organization = factory.SubFactory(OrganizationFactory)
    active = True

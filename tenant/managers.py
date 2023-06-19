from django.db.models import Manager


class MainUserManager(Manager):

    def find_or_create(self, user_id, organization_id):
        if not organization_id:
            raise ValueError("organization not detected")
        if not user_id:
            raise ValueError('userID not detected')

    def create_user(self, user_id, organization_id):
        if not organization_id:
            raise ValueError("organization not detected")
        if not user_id:
            raise ValueError('userID not detected')
        user = self.model(user_id=user_id, organization_id=organization_id)
        user.save(using=self._db)
        return user

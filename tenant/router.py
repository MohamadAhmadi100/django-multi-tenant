from threading import local

_thread_locals = local()


def set_organization(organization):
    _thread_locals.organization = organization


def get_organization():
    return getattr(_thread_locals, 'organization', None)


class OrganizationDatabaseRouter:
    def _get_db_alias(self):
        organization = get_organization()
        if organization:
            return organization.database_alias
        else:
            return 'default'

    def db_for_read(self, model, **hints):
        return self._get_db_alias()

    def db_for_write(self, model, **hints):
        return self._get_db_alias()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

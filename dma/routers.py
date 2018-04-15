
class VirvoRouter:
    """
    A router to control all database operations on models in the
    virvo application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read virvo models go to virvo.
        """
        if model._meta.app_label == 'virvo':
            return 'virvo'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write virvo models go to virvo.
        """
        if model._meta.app_label == 'virvo':
            return 'virvo'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the virvo app is involved.
        """
        if obj1._meta.app_label == 'virvo' or \
           obj2._meta.app_label == 'virvo':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the virvo app only appears in the 'virvo'
        database.
        """
        if app_label == 'virvo':
            return db == 'virvo'
        return None
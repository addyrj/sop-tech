from .middleware import get_current_client


class ClientRouter:

    def db_for_read(self, model, **hints):

        # system apps always in default DB
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return 'default'

        # fallback safe
        return get_current_client() or 'ambrane'


    def db_for_write(self, model, **hints):

        # system apps always in default DB
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return 'default'

        return get_current_client() or 'ambrane'


    def allow_relation(self, obj1, obj2, **hints):
        # allow relations only within same DB or safe fallback
        if obj1._state.db and obj2._state.db:
            return obj1._state.db == obj2._state.db
        return True


    def allow_migrate(self, db, app_label, model_name=None, **hints):

        # SYSTEM TABLES → ONLY default DB
        if app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return db == 'default'

        # YOUR APP → client DBs (ambrane, etc.)
        if app_label == 'sop':
            return db != 'default'

        return False
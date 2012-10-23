from psycopg2 import connect
import transaction


def eplasty_tween_factory(handler, registry):
    def eplasty_tween(request):
        config=registry.settings
        conn = connect(
            host = config.get('postgres.host', '127.0.0.1'),
            port = config.get('postgres.port', '5432'),
            database = config['postgres.database'],
            user = config['postgres.username'],
            password = config['postgres.passwd'],
        )
        request.pg_transaction = conn
        transaction.roin(manager)
        return handler(request)
    return eplasty_tween

def includeme(config):
    config.add_tween(
        'pyramid_postgres.tween.eplasty_tween_factory',
        under='pyramid_tm.tm_tween_factory'
    )

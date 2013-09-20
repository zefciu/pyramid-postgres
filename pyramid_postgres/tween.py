import logging
from psycopg2 import connect, extensions, extras
import transaction

from pyramid_postgres.connection import PostgresManager

def _hide_problematic(item):
    """Converts items that can spoil logs to different form."""
    if isinstance(item, bytes):
        return '<{0} BYTES>'.format(len(item))
    return item

class LoggingCursor(extras.NamedTupleCursor):

    def __init__(self, *args, **kwargs):
        self.sql_logger = logging.getLogger('sql')
        self.err_logger = logging.getLogger('sql_errors')
        super(LoggingCursor, self).__init__(*args, **kwargs)

    def execute(self, sql, args=None):
        try:
            args_to_log = (
                args and tuple((_hide_problematic(item) for item in args))
            )
            command = self.mogrify(sql, args)
            command_to_log = self.mogrify(sql, args_to_log)
            self.sql_logger.info(command_to_log)
            super(LoggingCursor, self).execute(command)
        except Exception as exc:
            self.err_logger.error(exc)
            raise

class LoggingConnection(extensions.connection):
    def cursor(self, *args, **kwargs):
        kwargs.setdefault('cursor_factory', LoggingCursor)
        return super(LoggingConnection, self).cursor(*args, **kwargs)


def eplasty_tween_factory(handler, registry):
    def eplasty_tween(request):
        config=registry.settings
        conn = connect(
            host = config.get('postgres.host', '127.0.0.1'),
            port = config.get('postgres.port', '5432'),
            database = config['postgres.database'],
            user = config['postgres.username'],
            password = config['postgres.passwd'],
            connection_factory = LoggingConnection,
        )
        request.pg_connection = conn
        transaction.get().join(PostgresManager(
            conn, tpc=config.get('postgres.tpc', False)
        ))
        return handler(request)
    return eplasty_tween

def includeme(config):
    config.add_tween(
        'pyramid_postgres.tween.eplasty_tween_factory',
        under='pyramid_tm.tm_tween_factory'
    )

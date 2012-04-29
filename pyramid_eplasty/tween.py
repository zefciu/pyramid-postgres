from psycopg2 import connect
import eplasty as ep
import transaction

from pyramid_eplasty.data_manager import EPDataManager

def eplasty_tween_factory(handler, registry):
    def eplasty_tween(request):
        config=registry.settings
        conn = connect(
            host = config.get('eplasty.host', '127.0.0.1'),
            port = config.get('eplasty.port', '5432'),
            database = config['eplasty.database'],
            user = config['eplasty.username'],
            password = config['eplasty.passwd'],
            connection_factory=ep.cursor.EPConnection
        )
        manager = EPDataManager(conn)
        transaction.join(manager)
        return handler(request)

def includeme(config):
    config.add_tween(eplasty_tween_factory)

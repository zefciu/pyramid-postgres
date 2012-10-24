import random
from string import ascii_lowercase

class PostgresManager():

    def __init__(self, connection):
        self.connection = connection
        self.xid = ''.join(
            random.choice(ascii_lowercase) for i in range(32)
        )
        self.connection.tpc_begin(self.xid)

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        self.connection.tpc_prepare()

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        self.connection.tpc_commit()

    def abort(self, transaction):
        self.connection.rollback()

    def tpc_abort(self, transaction):
        self.connection.rollback()

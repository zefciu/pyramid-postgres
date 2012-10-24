import random
from string import ascii_lowercase

class PostgresManager():

    def __init__(self, connection, tpc=False):
        self.connection = connection
        self.tpc = tpc
        if tpc:
            self.connection.tpc_begin(self.xid)
            self.xid = ''.join(
                random.choice(ascii_lowercase) for i in range(32)
            )

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        if self.tpc:
            self.connection.tpc_prepare()

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        if self.tpc:
            self.connection.tpc_commit()
        else:
            self.connection.commit()

    def abort(self, transaction):
        self.connection.rollback()

    def tpc_abort(self, transaction):
        if self.tpc:
            self.connection.tpc_rollback()
        else:
            self.connection.rollback()

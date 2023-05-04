from sqlalchemy import event


class QueryCounter(object):
    """Context manager to count SQLALchemy queries."""

    def __init__(self, session):
        self.connection = session.connection()
        self.count = 0

    def __enter__(self):
        event.listen(self.connection, "before_cursor_execute", self.callback)
        return self

    def __exit__(self, *args, **kwargs):
        event.remove(self.connection, "before_cursor_execute", self.callback)

    def callback(self, *args, **kwargs):
        self.count += 1

from quart import session
import secrets

__all__ = ["SessionResource"]

ID_KEY = "resource_id"

# TODO is there a less dumb way to do this?
# TODO clean up periodically to avoid leaking memory
class SessionResource():
    """
    Store resources on a per-session basis.
    Unlike with the quart-session extension, these are not deserialized each request.
    """

    def __init__(self, new_resource, *args, **kwargs):
        """
        Create empty storage. Extra arguments specify how to initialize resources

        Arguments
        =========
        new_resource : callable
            Function/constructor to creat a new resource
        args, kwargs
            Arguments to pass to new_resource
        """
        self.storage = dict()

        def init_func():
            return new_resource(*args, **kwargs)

        self.init_new = init_func

    @staticmethod
    def _new_id():
        return secrets.token_bytes(16)

    def get_resource(self):
        id = session.get(ID_KEY, None)
        if id is None:
            id = self._new_id()
            while id in session:
                newid = self._new_id()
            session[ID_KEY] = id
        if id not in self.storage:
            self.storage[id] = self.init_new()
        return self.storage[id]

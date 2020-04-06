class UserObject:
    """Represents a single connection.

    Usage of this object is similar to 'self', where this object stores the object
    references for things like ConstantSQL and Storage
    """

    def __init__(self, ws, clid, storage):
        self.uid = -1
        self.loggedIn = False
        self.username = ""
        self.ws = ws
        self.clid = clid
        self.curpath = ""
        self.groups = {}
        self.storage = storage

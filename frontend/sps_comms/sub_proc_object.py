class SubProcObject:
    """Represents a single submission processing server."""

    def __init__(self, ws, spid, spsName):
        """Initializer for SubProcObject.

        Args:
            ws: A websocket
            spid: The unique submission processing server id
            spsName: The submission processing server's reported name
        """
        self.ws = ws
        self.spid = spid
        self.spsName = spsName
        self.busy = False
        self.cursubid = -1

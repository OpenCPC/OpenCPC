class Storage:
    """Essentially stores globals."""

    def __init__(self, sql):
        """Initializer for Storage.

        Args:
            sql: A ConstantSQL object
        """
        self.all_sp = []
        self.unique_spid = 0

        self.all_cl = []
        self.unique_clid = 0

        self.sql = sql

        self.sdf_submission_dispatch_awaitable = None

    def get_new_unique_clid(self):
        """Generated a new unique client ID (relative to this Storage object).

        Returns:
            A unique integer relative to this function and this Storage object.
        """
        self.unique_clid += 1
        return self.unique_clid - 1

    def schedule_sdf(self):
        """Tells the submission dispatcher to run as soon as possible, if not already."""
        if self.sdf_submission_dispatch_awaitable:
            if not self.sdf_submission_dispatch_awaitable.done():
                self.sdf_submission_dispatch_awaitable.set_result(None)

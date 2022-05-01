from typing import Optional
from interface.iapp import IApp
from interface.igossipmanager import IGossipManager


class GossipManager(IGossipManager):

    def __init__(self):
        self.app: Optional[IApp] = None

    def set_app(self, app: IApp):
        self.app = app

    def start(self):
        """Starts the runnable object."""
        pass

    def stop(self):
        """Stops the runnable object."""
        pass

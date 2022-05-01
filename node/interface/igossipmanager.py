import abc

from interface.irunnable import IRunnable


class IGossipManager(IRunnable, metaclass=abc.ABCMeta):
    pass

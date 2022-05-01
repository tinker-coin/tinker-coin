import abc

from interface.inetworkinterface import INetworkInterface
from interface.irunnable import IRunnable


class INetworkedWorker(IRunnable, INetworkInterface, metaclass=abc.ABCMeta):
    pass


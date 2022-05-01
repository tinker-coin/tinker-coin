import abc


class IRunnable(metaclass=abc.ABCMeta):

    def start(self):
        """Starts the runnable object."""
        pass

    def stop(self):
        """Stops the runnable object."""
        pass

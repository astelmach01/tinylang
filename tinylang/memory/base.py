import abc


class BaseMemory(abc.ABC):
    @abc.abstractmethod
    def add_user_message(self, message):
        pass

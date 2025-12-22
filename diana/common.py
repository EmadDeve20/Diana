class Singleton:
    _instance = None

    def __new__(cls):

        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


class Borg(Singleton):
    _shared_state: dict = {}

    def __init__(self) -> None:
        self.__dict__ = self._shared_state


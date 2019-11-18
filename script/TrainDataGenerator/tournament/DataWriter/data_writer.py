from abc import ABCMeta, abstractclassmethod


class DataWriterException(Exception):
    pass


class DataWriter(metaclass=ABCMeta):
    @abstractclassmethod
    def write(self, scored_player_list: list):
        pass

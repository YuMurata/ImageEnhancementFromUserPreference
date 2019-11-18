from threading import Thread
import json
from .data_writer import DataWriter, DataWriterException
from pathlib import Path


class ScoredParamWriterException(DataWriterException):
    pass


SUFFIX = '.json'


class WriteThread(Thread):
    def __init__(self, scored_player_list: list, save_file_path: str):
        super(WriteThread, self).__init__()
        self.scored_player_list = scored_player_list
        self.save_file_path = save_file_path

    def run(self):
        score = 'score'
        param = 'param'
        save_list = [{score: player[score], param:player[param]}
                     for player in self.scored_player_list]

        with open(self.save_file_path, 'w') as fp:
            json.dump(save_list, fp, indent=4)


class ScoredParamWriter(DataWriter):
    def __init__(self, save_file_path: str):
        if Path(save_file_path).suffix != SUFFIX:
            raise ScoredParamWriterException(f'suffix is not {SUFFIX}')

        self.save_file_path = save_file_path

    def write(self, scored_player_list: list):
        write_thread = WriteThread(scored_player_list, self.save_file_path)
        write_thread.start()

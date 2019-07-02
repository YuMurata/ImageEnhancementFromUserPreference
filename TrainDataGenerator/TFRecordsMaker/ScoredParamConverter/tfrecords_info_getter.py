from tkinter import Tk
import tensorflow as tf
from pathlib import Path

from TrainDataGenerator.TFRecordsMaker.util \
    import get_dataset_dir, DATASET_TYPE_LIST, EXTENSION


def disp_tfrecords_length(tfrecord_dir_path: str):
    tfrecord_dir_path = Path(tfrecord_dir_path)

    assert tfrecord_dir_path.exists()

    print(f'directory: {tfrecord_dir_path}')
    for dataset_type in DATASET_TYPE_LIST:
        dataset_length = \
            len(list(tf.python_io.tf_record_iterator(
                str(tfrecord_dir_path/(dataset_type+EXTENSION)))))
        print(f'{dataset_type} length: {dataset_length}' % (dataset_type, dataset_length))

if __name__ == "__main__":
    root = Tk()
    root.attributes('-topmost', True)

    root.withdraw()
    root.lift()
    root.focus_force()

    dataset_dir = get_dataset_dir()
    root.destroy()

    disp_tfrecords_length(dataset_dir)

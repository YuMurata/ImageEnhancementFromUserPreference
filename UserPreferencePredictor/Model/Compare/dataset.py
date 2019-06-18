import tensorflow as tf
from TrainDataGenerator.TFRecordsMaker.util \
    import IMAGE_CHANNEL, IMAGE_HEIGHT, IMAGE_WIDTH


class TrainDataset:
    def __init__(self, graph: tf.Graph, batch_size: int):
        self.batch_size = batch_size
        with graph.as_default():
            with tf.variable_scope('train_data_set'):
                self.file_path_placeholder = \
                    tf.placeholder(tf.string, shape=[None], name='file_path')

                dataset = self._make_dataset()

                iterator = \
                    tf.data.Iterator.from_structure(
                        dataset.output_types, dataset.output_shapes)
                self.left_image, self.right_image, self.label = \
                    iterator.get_next()
                self.init_op = iterator.make_initializer(dataset)

    def _make_dataset(self):
        dataset = \
            tf.data.TFRecordDataset(self.file_path_placeholder) \
            .map(self._parse_function) \
            .map(self._read_image) \
            .shuffle(self.batch_size) \
            .batch(self.batch_size)
        return dataset

    def _parse_function(self, example_proto):
        features = {
            'label': tf.FixedLenFeature((), tf.int64, default_value=0),
            'left_image': tf.FixedLenFeature((), tf.string, default_value=""),
            'right_image': tf.FixedLenFeature((), tf.string, default_value=""),
        }
        parsed_features = tf.parse_single_example(example_proto, features)

        return parsed_features

    def _read_image(self, parsed_features):
        left_image_raw = \
            tf.decode_raw(parsed_features['left_image'], tf.uint8)
        right_image_raw =\
            tf.decode_raw(parsed_features['right_image'], tf.uint8)

        label = tf.cast(parsed_features['label'], tf.int32, name='label')

        float_left_image_raw = tf.cast(left_image_raw, tf.float32)/255
        float_right_image_raw = tf.cast(right_image_raw, tf.float32)/255

        shape = [IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNEL]
        left_image = \
            tf.reshape(float_left_image_raw, shape, name='left_image')
        right_image = \
            tf.reshape(float_right_image_raw, shape, name='right_image')

        return left_image, right_image, label

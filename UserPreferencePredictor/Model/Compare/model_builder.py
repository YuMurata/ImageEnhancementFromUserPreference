import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path
from UserPreferencePredictor.Model.Compare.dataset \
    import TrainDataset, IMAGE_HEIGHT, IMAGE_WIDTH


class ModelBuilder:
    SCOPE = 'predict_model'

    def __init__(self, batch_size: int, graph: tf.Graph,
                 is_tensor_verbose=False):
        self.is_tensor_verbose = is_tensor_verbose

        with graph.as_default():
            with tf.variable_scope(ModelBuilder.SCOPE):
                self.train_dataset = TrainDataset(graph, batch_size)

                self._build_model()

                self.merged_summary = tf.summary.merge_all()

                all_variable = \
                    tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,
                                      scope=ModelBuilder.SCOPE)
                train_variable = \
                    tf.trainable_variables(scope=ModelBuilder.SCOPE)

                self.variables_init_op = \
                    tf.variables_initializer(all_variable)
                self.local_variables_init_op = tf.local_variables_initializer()

                self.saver = tf.train.Saver(train_variable)
                self.sess = tf.Session(graph=graph)

    def _build_evaluate_network(self, input_layer: tf.Tensor):
        array_height, array_width = IMAGE_HEIGHT, IMAGE_WIDTH

        conv1_filter_num = 32
        conv1_layer = \
            tf.layers.conv2d(
                inputs=input_layer, filters=conv1_filter_num, kernel_size=5,
                padding='same', activation=tf.nn.relu, name='conv1_layer')

        pooling1_layer = \
            tf.layers.max_pooling2d(
                inputs=conv1_layer, pool_size=2, strides=2,
                name='pooling1_layer')
        array_height, array_width = array_height//2, array_width//2

        conv2_filter_num = conv1_filter_num*2
        conv2_layer = \
            tf.layers.conv2d(
                inputs=pooling1_layer, filters=conv2_filter_num, kernel_size=5,
                padding='same', activation=tf.nn.relu, name='conv2_layer')

        pooling2_layer = \
            tf.layers.max_pooling2d(
                inputs=conv2_layer, pool_size=2, strides=2,
                name='pooling2_layer')
        array_height, array_width = array_height//2, array_width//2

        flatten_layer = \
            tf.reshape(
                pooling2_layer,
                shape=[-1, array_height*array_width*conv2_filter_num],
                name='flatten_layer')

        dense_layer = \
            tf.layers.dense(
                inputs=flatten_layer, units=1024,
                activation=tf.nn.relu, name='dense_layer')
        dropout_layer = \
            tf.layers.dropout(
                inputs=dense_layer,
                rate=self.dropout_placeholder, name='dropout_layer')

        output_layer = tf.layers.dense(
            dropout_layer, units=1, activation=None, name='output_layer')

        if self.is_tensor_verbose:
            print('--- evaluate network ---')
            print(conv1_layer)
            print(pooling1_layer)
            print(conv2_layer)
            print(pooling2_layer)
            print(flatten_layer)
            print(dense_layer)
            print(dropout_layer)
            print(output_layer)
            print('')

        return output_layer

    def _build_loss_func(
            self, stacked_evaluate: tf.Tensor):
        data_loss = \
            tf.nn.sparse_softmax_cross_entropy_with_logits(
                logits=stacked_evaluate, labels=self.train_dataset.label,
                name='data_loss')

        self.loss_op = tf.reduce_mean(data_loss)
        tf.summary.scalar('loss', self.loss_op)

        global_step = tf.train.get_or_create_global_step()
        self.train_op = \
            tf.train.AdamOptimizer() \
            .minimize(self.loss_op, global_step=global_step)

        if self.is_tensor_verbose:
            print('--- loss func ---')
            print(stacked_evaluate)
            print(data_loss)
            print('')

    def _build_metrics(
            self, stacked_evaluate: tf.Tensor):
        predict_label = \
            tf.cast(
                tf.argmax(stacked_evaluate, axis=1),
                tf.int32, name='predict_label')

        metrics_name_list = ['accuracy', 'recall', 'precision']
        metrics_func_list = \
            [tf.metrics.accuracy, tf.metrics.recall, tf.metrics.precision]

        metrics_dict, update_dict = {}, {}
        for name, func in zip(metrics_name_list, metrics_func_list):
            metrics_dict[name], update_dict[name] = \
                func(self.train_dataset.label, predict_label, name=name)

        entire_update_op = tf.group(*update_dict.values())

        if self.is_tensor_verbose:
            print('--- metrics ---')
            print(stacked_evaluate)
            print(predict_label)
            print(self.train_dataset.label)
            for value in metrics_dict.values():
                print(value)
            print('')

        return metrics_dict, entire_update_op

    def _build_model(self):
        with tf.variable_scope('placeholder'):
            self.dropout_placeholder = tf.placeholder(tf.float32)

        with tf.variable_scope('evaluate_network'):
            if self.is_tensor_verbose:
                print('left')
            with tf.variable_scope('left_network'):
                self.left_evaluate_net = \
                    self._build_evaluate_network(
                        self.train_dataset.left_image)

            if self.is_tensor_verbose:
                print('right')
            with tf.variable_scope('right_network'):
                right_evaluate_net = \
                    self._build_evaluate_network(
                        self.train_dataset.right_image)

        with tf.variable_scope('evaluate'):
            left_evaluate = \
                tf.reduce_sum(
                    self.left_evaluate_net, axis=1, name='left_evaluate')
            right_evaluate = \
                tf.reduce_sum(
                    right_evaluate_net, axis=1, name='right_evaluate')
            stacked_evaluate = \
                tf.stack(
                    [left_evaluate, right_evaluate], axis=1,
                    name='stacked_evaluate')

        with tf.variable_scope('loss_function'):
            self._build_loss_func(stacked_evaluate)

        with tf.variable_scope('metrics'):
            if self.is_tensor_verbose:
                print('train')
            with tf.variable_scope('train_metrics'):
                self.train_metrics_dict, self.train_metrics_update = \
                    self._build_metrics(stacked_evaluate)
                for key, value in self.train_metrics_dict.items():
                    tf.summary.scalar(key, value, family='metrics')

            if self.is_tensor_verbose:
                print('test')
            with tf.variable_scope('test_metrics'):
                self.test_metrics_dict, self.test_metrics_update = \
                    self._build_metrics(stacked_evaluate)

    def _image_to_array(self, image: Image):
        resized_image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        return np.asarray(resized_image).astype(np.float32)/255

    def initialize_metrics(self):
        self.sess.run(self.local_variables_init_op)

    def restore(self, check_point_path: str):
        self.saver.restore(
            self.sess, str(Path(check_point_path).joinpath('save')))


if __name__ == '__main__':
    load_dir = str(Path(__file__).parent/'predict_model_test')
    graph = tf.Graph()
    print(ModelBuilder(1, graph).restore(load_dir))

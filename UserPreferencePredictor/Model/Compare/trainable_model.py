import tensorflow as tf
from tqdm import tqdm, trange
from pathlib import Path

from UserPreferencePredictor.Model.Compare.model_builder \
    import ModelBuilder


class TrainableModel(ModelBuilder):
    def __init__(self, batch_size: int, summary_dir: str, graph=None,
                 is_tensor_verbose=False, is_use_jupyter=False):

        if graph is None:
            graph = tf.get_default_graph()

        super(TrainableModel, self).__init__(
            batch_size, graph, is_tensor_verbose)

        self.summary_writer = \
            tf.summary.FileWriter(summary_dir, self.sess.graph)

        self.is_use_jupyter = is_use_jupyter

    def initialize_variable(self):
        super(TrainableModel, self).initialize_metrics()
        self.sess.run(self.variables_init_op)

    def _batch_train(self, progress: tqdm):
        fetch_list = [self.train_op, self.train_metrics_update,
                      self.loss_op, self.merged_summary,
                      tf.train.get_global_step(self.sess.graph)]

        try:
            while True:
                _, _, loss, summary, global_step = \
                    self.sess.run(fetch_list,
                                  feed_dict={
                                      self.dropout_placeholder: 0.5
                                  })

                info_list = [('loss', loss)]
                info_list.extend([(key, self.sess.run(value))
                                  for key, value
                                  in self.train_metrics_dict.items()])

                if progress is not None:
                    progress.update()
                    progress.set_postfix(info_list)

                self.summary_writer.add_summary(
                    summary, global_step=global_step)

        except tf.errors.OutOfRangeError:
            return loss

    def fit(self, train_dataset_path: str, epoch_num: int) -> dict:
        print('--- train ---')

        for epoch in trange(epoch_num, desc='epoch'):
            self.sess.run(
                self.train_dataset.init_op,
                feed_dict={
                    self.train_dataset.file_path_placeholder:
                    [train_dataset_path]})

            progress = tqdm(desc='batch') if not self.is_use_jupyter else None
            loss = self._batch_train(progress)
            if progress is not None:
                progress.close()

        print('\n')
        ret_metrics = {key: self.sess.run(value)
                       for key, value in self.train_metrics_dict.items()}
        ret_metrics['loss'] = loss
        return ret_metrics

    def save(self, save_path: str):
        self.saver.save(self.sess, str(Path(save_path).joinpath('save')))

    def inference(self, test_dataset_path: str):
        print('--- inference ---')

        self.sess.run(self.train_dataset.init_op,
                      feed_dict={
                          self.train_dataset.file_path_placeholder:
                          [test_dataset_path]})
        with tqdm(desc='batch') as pbar:
            try:
                while True:
                    self.sess.run(
                        self.test_metrics_update,
                        feed_dict={
                            self.dropout_placeholder: 0
                        })
                    pbar.update()
                    info_list = \
                        ([(key, self.sess.run(value))
                            for key, value in self.test_metrics_dict.items()])
                    pbar.set_postfix(info_list)

            except tf.errors.OutOfRangeError:
                pass

        print('')

        return {key: self.sess.run(value)
                for key, value in self.test_metrics_dict.items()}


if __name__ == '__main__':
    from tkinter import filedialog
    from pprint import pprint

    summary_dir = str(Path(__file__).parent/'predict_model_test')
    batch_size = 2
    predict_model = TrainableModel(batch_size, summary_dir)
    predict_model.initialize_variable()

    tfrecords_path = \
        filedialog.askopenfilename(
            title='select tfrecords', filetypes=[('', '.tfrecords')])

    epoch_num = 20
    loss, metrics = predict_model.fit(tfrecords_path, epoch_num)
    print('loss: %f' % loss)
    pprint(metrics)

    predict_model.save(summary_dir)
    predict_model.restore(summary_dir)

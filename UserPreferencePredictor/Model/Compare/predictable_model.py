from UserPreferencePredictor.Model.Compare.model_builder \
    import ModelBuilder, tf


class PredictableModel(ModelBuilder):
    def __init__(self, graph=None, is_tensor_verbose=False):
        if graph is None:
            graph = tf.get_default_graph()
        super(PredictableModel, self).__init__(0, graph, is_tensor_verbose)

    def predict_evaluate(self, data_list: list):
        feed_dict = {
            self.train_dataset.left_image:
                [self._image_to_array(data['image']) for data in data_list],
            self.dropout_placeholder: 0
        }

        return self.sess.run(self.left_evaluate_net, feed_dict=feed_dict)


if __name__ == '__main__':
    from PIL import Image
    from tkinter import filedialog
    from pathlib import Path

    predict_model = PredictableModel()

    load_dir = str(Path(__file__).parent/'predict_model_test')
    if not load_dir:
        exit()

    predict_model.restore(load_dir)

    image_path = \
        filedialog.askopenfilename(
            title='select image', filetypes=[('', ['.jpg', 'png'])])
    print(predict_model.predict_evaluate([{'image': Image.open(image_path)}]))

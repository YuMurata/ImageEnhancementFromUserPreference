import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def hist_match(source, template):
    """
    Adjust the pixel values of a grayscale image such that its histogram
    matches that of a target image

    Arguments:
    -----------
        source: np.ndarray
            Image to transform; the histogram is computed over the flattened
            array
        template: np.ndarray
            Template image; can have different dimensions to source
    Returns:
    -----------
        matched: np.ndarray
            The transformed output image
    """

    oldshape = source.shape
    source = source.ravel()
    template = template.ravel()

    # get the set of unique pixel values and their corresponding indices and
    # counts
    s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                            return_counts=True)
    t_values, t_counts = np.unique(template, return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    return interp_t_values[bin_idx].reshape(oldshape)


if __name__ == "__main__":
    src = Image.open(
        r'C:\Users\init\Documents\研究\人の好みに基づく評価関数の推定\研究成果\画像\ヒストグラムマッチング\src.png').convert('RGB')
    src_r, src_g, src_b = map(np.array, src.split())

    tar = Image.open(
        r'C:\Users\init\Documents\研究\人の好みに基づく評価関数の推定\研究成果\画像\ヒストグラムマッチング\tar.png').convert('RGB')
    tar_r, tar_g, tar_b = map(np.array, tar.split())

    mat_r, mat_g, mat_b = hist_match(tar_r, src_r), hist_match(
        tar_g, src_g), hist_match(tar_b, src_b)

    mat = Image.fromarray(np.stack([mat_r, mat_g, mat_b], 2).astype(np.uint8))

    plt.figure()
    plt.title('source')
    plt.imshow(np.array(src))

    plt.figure()
    plt.title('target')
    plt.imshow(np.array(tar))

    plt.figure()
    plt.title('match')
    plt.imshow(np.array(mat))

    plt.show()

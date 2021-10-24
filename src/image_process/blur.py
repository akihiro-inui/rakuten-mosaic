import numpy as np
import scipy.ndimage


def gaussian_blur(sharp_image, sigma):
    # Filter channels individually to avoid gray scale images
    blurred_image_r = scipy.ndimage.filters.gaussian_filter(sharp_image[:, :, 0], sigma=sigma)
    blurred_image_g = scipy.ndimage.filters.gaussian_filter(sharp_image[:, :, 1], sigma=sigma)
    blurred_image_b = scipy.ndimage.filters.gaussian_filter(sharp_image[:, :, 2], sigma=sigma)
    blurred_image = np.dstack((blurred_image_r, blurred_image_g, blurred_image_b))
    return blurred_image


def uniform_blur(sharp_image, uniform_filter_size):
    # The multidimensional filter is required to avoid gray scale images
    multidim_filter_size = (uniform_filter_size, uniform_filter_size, 1)
    blurred_image = scipy.ndimage.filters.uniform_filter(sharp_image, size=multidim_filter_size)
    return blurred_image


def blur_image_locally(sharp_image: np.ndarray, mask: np.ndarray, use_gaussian_blur: bool, gaussian_sigma: float, uniform_filter_size: float) -> np.ndarray:
    """
    Apply mosaic effect to the input image
    :param sharp_image: Original image ndarray
    :param mask: Mask ndarray where 0 indicates blur and 1 non-blur. This should have the same shape as sharp_image
    :param use_gaussian_blur: Set True to use gaussian blur
    :param gaussian_sigma: Sigma
    :param uniform_filter_size: Filter size
    :return: Mosaic photo
    """
    one_values_f32 = np.full(sharp_image.shape, fill_value=1.0, dtype=np.float32)
    sharp_image_f32 = sharp_image.astype(dtype=np.float32)
    sharp_mask_f32 = mask.astype(dtype=np.float32)

    if use_gaussian_blur:
        blurred_image_f32 = gaussian_blur(sharp_image_f32, sigma=gaussian_sigma)
        blurred_mask_f32 = gaussian_blur(sharp_mask_f32, sigma=gaussian_sigma)

    else:
        blurred_image_f32 = uniform_blur(sharp_image_f32, uniform_filter_size)
        blurred_mask_f32 = uniform_blur(sharp_mask_f32, uniform_filter_size)

    blurred_mask_inverted_f32 = one_values_f32 - blurred_mask_f32
    weighted_sharp_image = np.multiply(sharp_image_f32, blurred_mask_f32)
    weighted_blurred_image = np.multiply(blurred_image_f32, blurred_mask_inverted_f32)
    locally_blurred_image_f32 = weighted_sharp_image + weighted_blurred_image

    locally_blurred_image = locally_blurred_image_f32.astype(dtype=np.uint8)

    return locally_blurred_image

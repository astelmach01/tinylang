from pathlib import Path

import cv2
import numpy as np
from PIL import Image as PillowImage
from skimage import data

from tinylang.images import Image

# Set random seed for reproducibility
np.random.seed(42)

RESOURCES_DIR = (Path(__file__).parent.parent / "resources").resolve()


class TestImage:
    def test_from_to_numpy(self):
        np_arr = np.random.randint(0, 255, size=(100, 100), dtype=np.uint8)
        image = Image.from_numpy(np_arr)
        result_np = image.to_numpy()
        assert np.array_equal(np_arr, result_np)

    def test_from_pillow(self):
        pil_img = PillowImage.new("L", (100, 100))
        image = Image.from_pillow(pil_img)
        assert isinstance(image, Image)

    def test_from_opencv(self):
        cv2_arr = cv2.imread(
            str((RESOURCES_DIR / "image.png").resolve()), cv2.IMREAD_GRAYSCALE
        )  # Assuming grayscale
        image = Image.from_opencv(cv2_arr)
        assert isinstance(image, Image)

    def test_from_skimage(self):
        skimage_arr = data.camera()
        image = Image.from_skimage(skimage_arr)
        assert isinstance(image, Image)

    def test_from_bytes(self):
        with open(RESOURCES_DIR / "image.png", "rb") as f:
            image_bytes = f.read()
        image = Image.from_bytes(image_bytes)
        assert isinstance(image, Image)

    def test_to_from_dict(self):
        np_arr = np.random.randint(0, 255, size=(100, 100), dtype=np.uint8)
        image = Image.from_numpy(np_arr)
        serialized = image.to_dict()
        deserialized_image = Image.from_dict(serialized)
        assert np.array_equal(image.to_numpy(), deserialized_image.to_numpy())

    def test_str_representation(self):
        np_arr = np.random.randint(0, 255, size=(100, 100), dtype=np.uint8)
        image = Image(np_arr)
        assert "tinylang.images.Image object of size: (100, 100)" in str(image)

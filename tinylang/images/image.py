import base64
import io

import numpy as np
from PIL import Image as PillowImage


class Image:
    def __init__(self, image_data: np.ndarray) -> None:
        self.image_data = image_data

    def to_numpy(self) -> np.ndarray:
        return self.image_data

    @classmethod
    def from_pillow(cls, image_data: PillowImage) -> "Image":  # type: ignore
        return cls(np.array(image_data))

    @classmethod
    def from_opencv(cls, opencv_image: np.ndarray) -> "Image":
        return cls(opencv_image)

    @classmethod
    def from_numpy(cls, np_image_data: np.ndarray) -> "Image":
        return cls(np_image_data)

    @classmethod
    def from_bytes(cls, image_bytes: bytes) -> "Image":
        pillow_image = PillowImage.open(io.BytesIO(image_bytes))
        return cls(np.array(pillow_image))

    @classmethod
    def from_skimage(cls, skimage_image: np.ndarray) -> "Image":
        return cls(skimage_image)

    def to_dict(self) -> dict:
        """
        Convert the Image object to a dictionary format suitable for JSON serialization.
        """
        # Convert the numpy array to bytes, then encode to base64 string
        raw_bytes = self.image_data.tobytes()
        base64_encoded = base64.b64encode(raw_bytes).decode("utf-8")
        return {
            "image_data": base64_encoded,
            "dtype": str(self.image_data.dtype),
            "shape": self.image_data.shape,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Image":
        """
        Construct an Image object from a dictionary (produced by to_dict).
        """
        # Decode the base64 string to bytes, then convert to numpy array
        raw_bytes = base64.b64decode(data["image_data"])
        decoded_array = np.frombuffer(raw_bytes, dtype=data["dtype"]).reshape(
            data["shape"]
        )
        return cls(decoded_array)

    def __str__(self) -> str:
        return f"tinylang.images.Image object of size: {self.image_data.shape}"

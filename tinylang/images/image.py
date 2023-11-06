import base64
import io
import os
from pathlib import Path
from typing import Dict

import numpy as np
from PIL import Image as PillowImage


class Image:
    def __init__(
        self,
        image_bytes: bytes,
        format: str = "JPEG",
        image_dir: os.PathLike = Path(__name__).parent.parent,
    ) -> None:
        self.image_bytes = image_bytes
        self.format = format.upper()
        self.image_dir = image_dir

    def to_numpy(self) -> np.ndarray:
        with io.BytesIO(self.image_bytes) as image_io:
            with PillowImage.open(image_io) as pil_image:
                return np.array(pil_image.convert("RGB"))

    def to_b64(self) -> str:
        return base64.b64encode(self.image_bytes).decode("utf-8")

    @classmethod
    def from_pillow(cls, pil_image: PillowImage, format: str = "JPEG") -> "Image":
        with io.BytesIO() as output:
            pil_image.save(output, format=format)
            return cls(output.getvalue(), format)

    @classmethod
    def from_opencv(cls, opencv_image: np.ndarray, format: str = "JPEG") -> "Image":
        pil_image = PillowImage.fromarray(opencv_image)
        return cls.from_pillow(pil_image, format)

    @classmethod
    def from_numpy(cls, np_image_data: np.ndarray, format: str = "JPEG") -> "Image":
        pil_image = PillowImage.fromarray(np_image_data)
        return cls.from_pillow(pil_image, format)

    @classmethod
    def from_bytes(cls, image_bytes: bytes) -> "Image":
        with io.BytesIO(image_bytes) as image_io:
            pil_image = PillowImage.open(image_io)
            format = pil_image.format
            if format not in ["JPEG", "PNG", "WEBP", "GIF"]:
                raise ValueError("Unsupported image format")
            return cls(image_bytes, format)

    def to_bytes(self) -> bytes:
        return self.image_bytes

    def to_dict(self) -> Dict:
        base64_encoded = self.to_b64()
        return {
            "image_data": base64_encoded,
            "dtype": str(self.to_numpy().dtype),
            "shape": self.to_numpy().shape,
            "format": self.format,
        }

    def to_url(self) -> str:
        return f"data:image/{self.format.lower()};base64,{self.to_b64()}"

    @classmethod
    def from_dict(cls, data: Dict) -> "Image":
        raw_bytes = base64.b64decode(data["image_data"])
        return cls(raw_bytes, data.get("format", "JPEG"))

    def __str__(self) -> str:
        return f"Image object with {self.format} format, size: {self.to_numpy().shape}"

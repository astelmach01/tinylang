# 🖼️ Working with Images in Tinylang

## 📝 Introduction

Tinylang provides a flexible interface for working with images. This guide will walk you through how to use images in various formats and include them in conversations.

## 🏁 Initializing an Image

Tinylang supports initializing images from various formats including NumPy arrays, Pillow images, OpenCV images, and more.

```python
from tinylang.images import Image
import numpy as np
import cv2
from PIL import Image as PillowImage
from skimage import io as skimage_io

# Initialize from NumPy array
np_image = np.array([[0, 1], [1, 0]])
image_from_numpy = Image.from_numpy(np_image)

# Initialize from Pillow Image
pillow_image = PillowImage.open("image.png")
image_from_pillow = Image.from_pillow(pillow_image)

# Initialize from OpenCV Image
cv2_image = cv2.imread("image.png")
image_from_opencv = Image.from_opencv(cv2_image)

# Initialize from skimage Image
skimage_image = skimage_io.imread("image.png")
image_from_skimage = Image.from_skimage(skimage_image)

# Initialize from bytes
bytes_image = open("image.png", "rb").read()
image_from_bytes = Image.from_bytes(bytes_image)
```

## 💬 Using Images in Conversations

Images can be included in user messages and stored in conversation memory.

```python
from tinylang.images import Image
from tinylang.messages import UserMessage
from tinylang.memory import ConversationMemory

memory = ConversationMemory(last_k=5)

chatGPT = OpenAI(
    model="gpt-3.5-turbo", openai_organization="", openai_api_key="", memory=memory
)

user_image = Image.from(np_image)

chatGPT.chat("What is this?", image=user_image)
```

## 🗺️ Next Steps

- Learn how to [work with Functions](functions.md)
- Dive into [ConversationMemory](conversation_memory.md)

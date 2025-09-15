from tensorflow.keras.layers import MaxPooling2D
import numpy as np

# Example input feature map
feature_map = np.array([
    [1, 3, 2, 9],
    [5, 6, 1, 7],
    [4, 2, 8, 6],
    [3, 5, 7, 2]
]).reshape(1, 4, 4, 1)

# Applying max pooling
max_pool = MaxPooling2D(pool_size=(2, 2), strides=2)
output = max_pool(feature_map)

print(output.numpy().reshape(2, 2))



import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import AveragePooling2D

feature_map = np.array([
    [1, 3, 2, 9],
    [5, 6, 1, 7],
    [4, 2, 8, 6],
    [3, 5, 7, 2]
], dtype=np.float32).reshape(1, 4, 4, 1)  # Convert to float32

# Applying average pooling
avg_pool = AveragePooling2D(pool_size=(2, 2), strides=2)
output = avg_pool(feature_map)
print(output.numpy().reshape(2, 2))
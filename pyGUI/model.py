import tensorflow as tf
from tensorflow.keras import layers, models
#from tensorflow.keras.datasets import mnist
from simulate import Simulate

# Simulate data
s = Simulate(maxObj=5, maxWidth=2, r=30)

s.simulate(100000)

# Load and preprocess the dataset

(x_train, y_train), (x_test, y_test) = s.load(split=0.3)
#x_train, x_test = x_train / 255.0, x_test / 255.0

# Reshape data for CNN
#x_train = x_train.reshape(-1, 28, 28, 1)
#x_test = x_test.reshape(-1, 28, 28, 1)

# Define the CNN model
model = models.Sequential([
    layers.Conv1D(32, 3, activation='relu', input_shape=(91, 1)),
    layers.MaxPooling1D(2),
    layers.Conv1D(64, 3, activation='relu'),
    layers.MaxPooling1D(2),
    layers.Conv1D(64, 3, activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(5, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)

model.export('objNumModel')

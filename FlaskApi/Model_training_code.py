import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os

# Constants
DATA_PATH = "combined_data_resampled.csv"
SAVED_MODEL_PATH = "Mymodel1.h5"
EPOCHS = 30  # Number of epochs
BATCH_SIZE = 32  # Batch size
PATIENCE = 10  # Patience for early stopping
LEARNING_RATE = 0.0001  # Learning rate
test_size = 0.2  # Test set size
validation_size = 0.2  # Validation set size
loss = "categorical_crossentropy"  # Loss function

# Load and prepare data
data = pd.read_csv(DATA_PATH).astype('float32')
X = data.drop('0', axis=1)  # Assuming '0' is the label column
y = data['0']

# Reshape the data
num_samples = X.shape[0]
num_features = X.shape[1]
# print(num_samples)
# print(num_features)
# Reshape X for the CNN model
X = np.reshape(X.values, (num_samples, num_features, 1))  # Reshaping to (num_samples, num_features, 1)

# Convert labels to categorical
y = tf.keras.utils.to_categorical(y, num_classes=16)  # 16 output classes

print("Training sets loaded!")

# Split the data into training, validation, and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=validation_size)

# Define the CNN model for the dataset
model = tf.keras.models.Sequential()

# 1st conv layer
model.add(tf.keras.layers.Conv1D(256, kernel_size=3, activation='relu', input_shape=(num_features, 1), padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.001)))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling1D(pool_size=2, strides=2, padding='same'))

# 2nd conv layer
model.add(tf.keras.layers.Conv1D(512, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.001)))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling1D(pool_size=2, strides=2, padding='same'))

# 3rd conv layer
model.add(tf.keras.layers.Conv1D(1024, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.001)))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling1D(pool_size=2, strides=2, padding='same'))

# Flatten the output and feed into dense layers
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(1024, activation='relu'))  # Dense layer with 512 units
model.add(tf.keras.layers.Dropout(0.5))

# Output layer with 16 classes
model.add(tf.keras.layers.Dense(16, activation='softmax'))

# Compile the model
optimiser = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
model.compile(optimizer=optimiser, loss=loss, metrics=["accuracy"])

# Print model summary
model.summary()

# Early stopping callback
earlystop_callback = tf.keras.callbacks.EarlyStopping(monitor="val_loss", min_delta=0.001, patience=PATIENCE)

# Train the model
history = model.fit(X_train,
                    y_train,
                    epochs=EPOCHS,
                    batch_size=BATCH_SIZE,
                    validation_data=(X_validation, y_validation),
                    callbacks=[earlystop_callback])

# Function to plot training history
def plot_history(history):
    fig, axs = plt.subplots(2)
    # Create accuracy subplot
    axs[0].plot(history.history["accuracy"], label="accuracy")
    axs[0].plot(history.history['val_accuracy'], label="val_accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("Accuracy evaluation")
    # Create loss subplot
    axs[1].plot(history.history["loss"], label="loss")
    axs[1].plot(history.history['val_loss'], label="val_loss")
    axs[1].set_xlabel("Epoch")
    axs[1].set_ylabel("Loss")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Loss evaluation")
    plt.show()

# Plot the training history
plot_history(history)

# Evaluate the network on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print("\nTest loss: {}, test accuracy: {}".format(test_loss, 100 * test_acc))

# Save the trained model
model.save(SAVED_MODEL_PATH)

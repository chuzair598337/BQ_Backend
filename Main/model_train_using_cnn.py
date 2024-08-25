import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os

currentFilePath = os.path.dirname(__file__)
DATA_PATH = "Model_data/Preprocess_Json_file4.json"
SAVED_MODEL_PATH = "Model_data/model4.h5"
EPOCHS = 15
BATCH_SIZE = 32
PATIENCE = 5
LEARNING_RATE = 0.001

def load_data(data_path):

    """Loads training dataset from json file.
    :param data_path (str): Path to json file containing data
    :return X (ndarray): Inputs
    :return y (ndarray): Targets
    """

    with open(data_path, "r") as fp:
        data = json.load(fp)

    X = np.array(data["MFCCs"])
    y = np.array(data["labels"])
    print("Training sets loaded!")
    return X, y


def prepare_dataset(data_path, test_size=0.2, validation_size=0.2):

    # load dataset
    X, y = load_data(data_path)

    # create train, validation, test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=validation_size)

    # add an axis to nd array
    X_train = X_train[..., np.newaxis]
    X_test = X_test[..., np.newaxis]
    X_validation = X_validation[..., np.newaxis]

    return X_train, y_train, X_validation, y_validation, X_test, y_test


def build_model(input_shape, loss="sparse_categorical_crossentropy", learning_rate=LEARNING_RATE):

    # build network architecture using convolutional layers
    model = tf.keras.models.Sequential()

    # 1st conv layer
    model.add(tf.keras.layers.Conv2D(128, (3, 3), activation='relu', input_shape=input_shape,
                                     kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2,2), padding='same'))

    # 2nd conv layer
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu',
                                     kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2,2), padding='same'))

    # 3rd conv layer
    model.add(tf.keras.layers.Conv2D(64, (2, 2), activation='relu',
                                     kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2,2), padding='same'))

    # flatten output and feed into dense layer
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    tf.keras.layers.Dropout(0.3)

    # softmax output layer
    model.add(tf.keras.layers.Dense(21, activation='softmax'))

    optimiser = tf.optimizers.Adam(learning_rate=learning_rate)

    # compile model
    model.compile(optimizer=optimiser,
                  loss=loss,
                  metrics=["accuracy"])

    # print model parameters on console
    model.summary()

    return model


def train(model, epochs, batch_size, patience, X_train, y_train, X_validation, y_validation):
    """Trains model
    :param epochs (int): Num training epochs
    :param batch_size (int): Samples per batch
    :param patience (int): Num epochs to wait before early stop, if there isn't an improvement on accuracy
    :param X_train (ndarray): Inputs for the train set
    :param y_train (ndarray): Targets for the train set
    :param X_validation (ndarray): Inputs for the validation set
    :param y_validation (ndarray): Targets for the validation set
    :return history: Training history
    """

    earlystop_callback = tf.keras.callbacks.EarlyStopping(monitor="accuracy", min_delta=0.001, patience=patience)

    # train model
    history = model.fit(X_train,
                        y_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        validation_data=(X_validation, y_validation),
                        callbacks=[earlystop_callback])
    return history


def plot_history(history):
    """Plots accuracy/loss for training/validation set as a function of the epochs
    :param history: Training history of model
    :return:
    """

    fig, axs = plt.subplots(2)

    # create accuracy subplot
    axs[0].plot(history.history["accuracy"], label="accuracy")
    axs[0].plot(history.history['val_accuracy'], label="val_accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("Accuracy evaluation")

    # create loss subplot
    axs[1].plot(history.history["loss"], label="loss")
    axs[1].plot(history.history['val_loss'], label="val_loss")
    axs[1].set_xlabel("Epoch")
    axs[1].set_ylabel("Loss")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Loss evaluation")

    plt.show()


def main():
    # generate train, validation and test sets
    X_train, y_train, X_validation, y_validation, X_test, y_test = prepare_dataset(DATA_PATH)

    # create network
    input_shape = (X_train.shape[1], X_train.shape[2], 1)
    model = build_model(input_shape, learning_rate=LEARNING_RATE)

    # train network
    history = train(model, EPOCHS, BATCH_SIZE, PATIENCE, X_train, y_train, X_validation, y_validation)

    # plot accuracy/loss for training/validation set as a function of the epochs
    plot_history(history)

    # evaluate network on test set
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print("\nTest loss: {}, test accuracy: {}".format(test_loss, 100*test_acc))

    # save model
    model.save(SAVED_MODEL_PATH)


if __name__ == "__main__":
    main()










# import json
# import numpy as np
# from sklearn.model_selection import train_test_split
# import tensorflow.keras as tf
#
# DATA_PATH = 'preprocessJson.json'
# SAVED_MODEL_PATH = "model.h5"
# LEARNING_RATE = 0.0001
# EPOCHS = 50
# BATCH_SIZE = 32
# NUM_KEYWORDS = 5
#
#
# def load_dataset(data_path):
#     with open(data_path, 'r') as fr:
#         data = json.load(fr)
#
#     X = np.array(data["MFCCs"])
#     Y = np.array(data["labels"])
#     return X, Y
#
#
# def get_data_splits(data_path, TEST_SIZE=0.1, TEST_VALIDATION=0.1):
#     X, y = load_dataset(data_path)
#
#     X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=TEST_SIZE)
#     X_train, X_validation, Y_train, Y_validation = train_test_split(X_train, Y_train, test_size=TEST_VALIDATION)
#
#     X_train = X_train[..., np.newaxis]
#     X_validation = X_validation[..., np.newaxis]
#     X_test = X_test[..., np.newaxis]
#     print(f"X_train {X_train}, X_validation {X_validation}, X_test {X_test}")
#     print(f"Y_train {Y_train}, Y_validation {X_validation}, Y_test {X_test}")
#     return X_train, X_validation, X_test, Y_train, Y_validation, Y_test
#
#
# def build_model(input_shape, learning_rate, error="sparse_categorical_crossentropy"):
#     model = tf.Sequential()
#
#     # add Model Layer 1
#     model.add(tf.layers.Conv2D(64, (3, 3), activation='relu', input_shape=input_shape,
#                                kernel_regularizer=tf.regularizers.l2(0.001)))
#     model.add(tf.layers.BatchNormalization())
#     model.add(tf.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))
#
#     # add Model Layer 2
#     model.add(tf.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape,
#                                kernel_regularizer=tf.regularizers.l2(0.001)))
#     model.add(tf.layers.BatchNormalization())
#     model.add(tf.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))
#
#     # add Model Layer 3
#     model.add(tf.layers.Conv2D(32, (2, 2), activation='relu', input_shape=input_shape,
#                                kernel_regularizer=tf.regularizers.l2(0.001)))
#     model.add(tf.layers.BatchNormalization())
#     model.add(tf.layers.MaxPool2D((2, 2), strides=(2, 2), padding="same"))
#
#     # add model flatten
#     model.add(tf.layers.Flatten())
#     model.add(tf.layers.Dense(64, activation="relu"))
#     model.add(tf.layers.Dropout(0.3))
#
#     model.add(tf.layers.Dense(NUM_KEYWORDS, activation="softmax"))
#
#     optimiser = tf.optimizers.Adam(learning_rate=learning_rate)
#     model.compile(optimizer=optimiser, loss=error, metrics='accuracy')
#     model.summary()
#     return model
#
#
# def main():
#     X_train, X_validation, X_test, Y_train, Y_validation, Y_test = get_data_splits(DATA_PATH)
#
#     input_shape = (X_train.shape[1], X_train.shape[2], X_train.shape[3])
#
#     model = build_model(input_shape, LEARNING_RATE)
#
#     model.fit(X_train, Y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_validation, Y_validation))
#
#     test_error, test_accuracy = model.evaluate(X_test, Y_test)
#     print(f"test Error:{test_error}, test_accuracy:{test_accuracy}")
#
#     model.save(SAVED_MODEL_PATH)
#
#
# if __name__=="__main__":
#     main()
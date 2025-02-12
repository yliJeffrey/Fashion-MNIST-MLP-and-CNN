# Convolutional neural network (CNN) for Fashion-MNIST dataset with random dropout
# 0.42M parameters with random initialization
# 2 convolutional layers: 32 + 64 filters
# 1 fully connected layer: 128 units
# EarlyStopping(patience=20)
# loss: 0.1567 - accuracy: 0.9398 - val_loss: 0.2027 - val_accuracy: 0.9292 - 6s/epoch - 12ms/step
# batch_size=128, epochs=300
# best result obtained at epoch 146

import numpy as np
import matplotlib.pyplot as plt
from keras.utils import to_categorical, plot_model
from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.callbacks import EarlyStopping, ModelCheckpoint

def load_data():
    (X_train, Y_train), (X_test, Y_test) = fashion_mnist.load_data()
    X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32') / 255
    X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32') / 255
    Y_train = to_categorical(Y_train)                       # one-hot encoding
    Y_test = to_categorical(Y_test)
    return (X_train, Y_train), (X_test, Y_test)

def create_model():
    model = Sequential()
    # convoluted layer 1
    model.add(Conv2D(filters=32,
                    kernel_size=(3,3),
                    padding='same',     # same size as the image
                    input_shape=(28,28,1),
                    activation='relu'))
    model.add(Dropout(0.5))     # random dropout
    model.add(MaxPool2D(pool_size=(2,2)))

    # convoluted layer 2
    model.add(Conv2D(filters=64,
                     kernel_size=(3, 3),
                     padding='same',      # same size as the image
                     activation='relu'))
    model.add(Dropout(0.6))     # random dropout
    model.add(MaxPool2D(pool_size=(2,2)))

    model.add(Flatten())

    # fully connected layer
    model.add(Dense(units=128,
                    kernel_initializer='normal',
                    activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(units=10,
                    kernel_initializer='normal',
                    activation='softmax'))
    print(model.summary())  # summary of model
    plot_model(model, to_file='network/fmc1.png', show_shapes=True)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',         # gradient descent
                  metrics=['accuracy'])
    return model

def train(model, batch_size, epochs, X_train, Y_train, X_test, Y_test):
    checkpoint = ModelCheckpoint('bestModel/fmc1.keras',
                                 monitor='val_loss',
                                 mode='min',
                                 save_best_only=True,
                                 verbose=1)
    early_stopping = EarlyStopping(patience=20)
    train_history = model.fit(x=X_train,
                              y=Y_train,
                              validation_data=(X_test, Y_test),
                              epochs=epochs,
                              batch_size=batch_size,
                              callbacks=[early_stopping, checkpoint],
                              verbose=2)
    return train_history

# evaluate model
def evaluate(model, X_test, Y_test):
    scores = model.evaluate(X_test, Y_test, verbose=0)
    return scores

def result_plt(hist):
    train_acc = hist.history['accuracy']
    val_acc = hist.history['val_accuracy']
    train_loss = hist.history['loss']
    val_loss = hist.history['val_loss']

    plt.figure(figsize=(9, 6))
    x = np.arange(len(train_loss))

    plt.subplot(1, 2, 1)
    plt.plot(x, train_acc)
    plt.plot(val_acc)
    plt.title("Train History of accuracy")
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train_acc', 'val_acc'], loc='lower right')

    plt.subplot(1, 2, 2)
    plt.plot(train_loss)
    plt.plot(val_loss)
    plt.title("Train History of loss")
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train_loss', 'val_loss'], loc='upper right')

    fig, loss_ax = plt.subplots()
    acc_ax = loss_ax.twinx()
    acc_ax.plot(train_acc, 'b', label='train_acc')
    acc_ax.plot(val_acc, 'g', label='val_acc')
    loss_ax.plot(train_loss, 'y', label='train_loss')
    loss_ax.plot(val_loss, 'r', label='val_loss')

    loss_ax.legend(loc='lower left')
    acc_ax.legend(loc='upper left')

    plt.show()


def main():
    (X_train, Y_train), (X_test, Y_test) = load_data()
    model = create_model()

    # (model, batch_size, epochs, X_train, Y_train, X_test, Y_test)
    hist = train(model, 128, 300, X_train, Y_train, X_test, Y_test)
    result_plt(hist)

    model.load_weights("bestModel/fmc1.keras")
    print("\nsaved model to disk")
    print("accuracy:", evaluate(model, X_test, Y_test)[1])

    # use model to predict
    index_list = np.random.choice(X_test.shape[0], 10)
    data = X_test[index_list]
    y_preds = model.predict(data)
    print("\npredicts===>>>")
    for i in range(10):
        print('True:' + str(np.argmax(Y_test[index_list[i]])) + 
              ', Predict:' + str(np.argmax(y_preds[i])) +
              ', index:' + str(index_list[i]))

if __name__ == "__main__":
    main()


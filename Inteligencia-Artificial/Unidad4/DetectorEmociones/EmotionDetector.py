
import cv2
import numpy as np
import tensorflow as tf
import keras as keras
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout,BatchNormalization, Input
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras import regularizers
from keras.callbacks import EarlyStopping

EMOCIONES = ['angry', 'disgusted', 'fearful', 'happy', 'neutral','sad','surprised']


IMG_SIZE = (48, 48)

TRAIN_DIR = 'dataset/train'
VAL_DIR = 'dataset/test'


def cargar_datos():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        brightness_range=(0.8, 1.2),
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=32,
        class_mode='categorical',
        color_mode='grayscale' 
    )

    test_gen = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=32,
        class_mode='categorical',
        color_mode='grayscale'  
    )

    return train_gen, test_gen


def construir_modelo(input_s,num_clases):
    model = Sequential()
    model.add(Input(shape=input_s))
    model.add(Conv2D(64, (4, 4), activation='elu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.3))
    
    model.add(Conv2D(64, (4, 4), activation='elu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.3))
    
    model.add(Conv2D(128, (3,3), activation='elu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.3))
    
    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
    model.add(Dropout(0.4))
    model.add(Dense(num_clases, activation='softmax'))

    optimizer = Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def entrenar_modelo(model, train_gen, test_gen, epochs=20):
    early_stop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)

    model.fit(
        train_gen,
        validation_data=test_gen,
        epochs=epochs,
        callbacks=[early_stop]
    )
    return model


def guardar_modelo(model, ruta='model/modelo_emociones.h5'):
    model.save(ruta)


def usar_modelo_webcam(ruta_modelo='model/modelo_emociones.h5'):
    model = load_model(ruta_modelo)

    detector_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = detector_rostros.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in rostros:
            rostro = gris[y:y+h, x:x+w]
            rostro_redim = cv2.resize(rostro, IMG_SIZE)
            rostro_redim = rostro_redim.astype("float32") / 255.0

            rostro_redim = np.expand_dims(rostro_redim, axis=-1)  # ahora (48,48,1)


            rostro_redim = np.expand_dims(rostro_redim, axis=0)   # ahora (1,48,48,1)


            pred = model.predict(rostro_redim)
            idx_emocion = np.argmax(pred)
            emocion = EMOCIONES[idx_emocion]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emocion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Detector de emociones", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


train_gen, test_gen = cargar_datos()
model = load_model('model/modelo_emociones.h5')
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)



usar_modelo_webcam('model/modelo_emociones.h5')
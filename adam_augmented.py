train_ds_path = "/home/beduinigor/target_dataset/train"
test_ds_path = "/home/beduinigor/target_dataset/test"

batch_size = 32
image_size = (240, 240)
epochs = 500

import os
from numpy import load

# ds_arrays_path = '/content/drive/MyDrive/TG/dataset_arraysTRAINING'
ds_arrays_path = '/home/beduinigor/dataset_arraysTRAINING'

X_train = load(os.path.join(ds_arrays_path,'x_train_data.npy'))
y_train = load(os.path.join(ds_arrays_path,'y_train_data.npy'))
X_test = load(os.path.join(ds_arrays_path,'x_test_data.npy'))
y_test = load(os.path.join(ds_arrays_path,'y_test_data.npy'))

from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5)

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import Model
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.class_weight import compute_class_weight
import autokeras as ak
import numpy as np
from pathlib import Path
import os

opt = 'Adam'
training_path = f"/home/beduinigor/training/{opt}"
model_path = "/home/beduinigor/tg2_COVIDNet/models/final_model.h5"

early_stop_callback = tf.keras.callbacks.EarlyStopping(
    monitor="loss",
    min_delta=0,
    patience=20,
    verbose=1,
    mode="auto",
    baseline=None,
    restore_best_weights=True)

augm_training_path = os.path.join(training_path, "augmented")

for train_method_path in [raw_training_path, augm_training_path]:
    for subdir in ['models', 'tensorboard']:
        if not os.path.isdir(os.path.join(train_method_path, subdir)):
            path = Path(os.path.join(train_method_path, subdir))
            path.mkdir(parents=True, exist_ok=True)

print("=============== AUGMENTED TRAINING ===============")
# augmented training
tensorboard_training_path = os.path.join(augm_training_path, 'tensorboard')
models_training_path = os.path.join(augm_training_path, 'models')
for i, (train_index, test_index) in enumerate(skf.split(X_train, y_train)):
    n_fold = i + 1
    print(f"\n\n\nFOLD {n_fold}")
    print("-------------------------------")

    model = load_model(model_path, custom_objects=ak.CUSTOM_OBJECTS)
    config = model.get_config()
    clean_model = Model.from_config(config)
    clean_model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    tb_fold_path = os.path.join(tensorboard_training_path, f"fold_{n_fold}")
    fold_path = os.path.join(models_training_path, f"fold_{n_fold}")
    if not os.path.isdir(fold_path):
        os.mkdir(fold_path)
    if not os.path.isdir(tb_fold_path):
        os.mkdir(tb_fold_path)


    x_train_fold = X_train[train_index]
    y_train_fold = to_categorical(y_train[train_index], 3)

    x_test_fold = X_train[test_index]
    y_test_fold = to_categorical(y_train[test_index], 3)

    print("Saving training fold nparrays...")
    np.save(os.path.join(fold_path, f"x_train_arr_augm_fold_{n_fold}.npy"), x_train_fold)
    np.save(os.path.join(fold_path, f"y_train_arr_augm_fold_{n_fold}.npy"), y_train_fold)
    np.save(os.path.join(fold_path, f"x_test_arr_augm_fold_{n_fold}.npy"), x_test_fold)
    np.save(os.path.join(fold_path, f"y_test_arr_augm_fold_{n_fold}.npy"), y_test_fold)
    print("Arrays saved with sucess!")


    print("\nStart training...")  
    print("Class weights:")
    class_weight = compute_class_weight(class_weight='balanced', classes=np.unique(y_train[train_index]), y=y_train[train_index])
    class_weight = {i: class_weight[i] for i in range(len(class_weight))}
    print(class_weight)


    tb_callback = tf.keras.callbacks.TensorBoard(
        log_dir=tb_fold_path,
        histogram_freq=0,
        write_graph=True,
        write_images=False,
        update_freq="epoch",
        profile_batch=2,
        embeddings_freq=0,
        embeddings_metadata=None)

    callbacks = [early_stop_callback, tb_callback]
    
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True)
    
    clean_model.fit(datagen.flow(x_train_fold, y_train_fold, batch_size=batch_size),
                epochs=epochs,
                validation_data=(x_test_fold, y_test_fold),
                callbacks=callbacks,
                class_weight=class_weight)

    print("\nSaving model...")
    try:
        clean_model.save(os.path.join(fold_path, f"model_fold_{n_fold}.h5"), save_format='h5')
        print("Model saved with sucess!")
    except:
        print("Fail trying to save the model!")
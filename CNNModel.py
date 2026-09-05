def main():

    import numpy as np
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Convolution2D
    from tensorflow.keras.layers import MaxPooling2D
    from tensorflow.keras.layers import Flatten
    # fixed import spacing
    from tensorflow.keras.layers import Dense, Dropout
    from tensorflow.keras import optimizers

    # new imports for report & confusion matrix
    from sklearn.metrics import classification_report, confusion_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns   # optional nicer heatmap (pip install seaborn)
    import os

    basepath = r"D:\Ai_real _img\newdataset"

    # Initialing the CNN
    classifier = Sequential()

    # Step 1 - Convolution Layer
    # Note: Your original used kernel (1,1). Keeping that, but you can change to (3,3) for better features.
    classifier.add(Convolution2D(32, 1, 1, input_shape=(100, 100, 3), activation='relu'))

    # step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding second convolution layer
    classifier.add(Convolution2D(32, 1, 1, activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Adding 3rd Convolution Layer
    classifier.add(Convolution2D(64, 1, 1, activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Step 3 - Flattening
    classifier.add(Flatten())

    # Step 4 - Full Connection
    classifier.add(Dense(256, activation='relu'))
    classifier.add(Dropout(0.5))
    classifier.add(Dense(2, activation='softmax'))  # change class no. if needed

    # Compiling The CNN
    classifier.compile(
        optimizer=optimizers.SGD(lr=0.01),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Part 2 Fitting the CNN to the image
    from keras.preprocessing.image import ImageDataGenerator
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    training_set = train_datagen.flow_from_directory(
        basepath + '/training_set',
        target_size=(100, 100),
        batch_size=32,
        class_mode='categorical')

    # IMPORTANT: set shuffle=False so predictions match test_set.classes order
    test_set = test_datagen.flow_from_directory(
        basepath + '/Testing_set',
        target_size=(100, 100),
        batch_size=32,
        class_mode='categorical',
        shuffle=False)

    steps_per_epoch = int(np.ceil(training_set.samples / 32))
    val_steps = int(np.ceil(test_set.samples / 32))

    # Fit (you used fit_generator — keep that if you prefer)
    model = classifier.fit_generator(
        training_set,
        steps_per_epoch=steps_per_epoch,
        epochs=199,
        validation_data=test_set,
        validation_steps=val_steps
    )

    # Saving the model
    classifier.save(basepath + '/fake_real_model.h5')

    # Evaluate and print accuracies
    scores = classifier.evaluate(test_set, verbose=1)
    B = "Testing Accuracy: %.2f%%" % (scores[1] * 100)
    print(B)
    scores = classifier.evaluate(training_set, verbose=1)
    C = "Training Accuracy: %.2f%%" % (scores[1] * 100)
    print(C)

    # ---------------------------
    # Classification report + Confusion matrix
    # ---------------------------

    # 1) Predict on test set (uses same ordering because shuffle=False)
    print("Running prediction on test set...")
    # use predict (predict_generator is deprecated in some TF versions)
    try:
        y_prob = classifier.predict(test_set, steps=val_steps, verbose=1)
    except Exception:
        # fallback to predict_generator if the environment requires it
        y_prob = classifier.predict_generator(test_set, steps=val_steps, verbose=1)

    y_pred = np.argmax(y_prob, axis=1)
    y_true = test_set.classes  # labels in the same order as files

    # 2) Get class names in index order
    # class_indices maps class_name -> index
    class_indices = test_set.class_indices
    # invert to get list where idx -> class_name
    idx_to_class = {v: k for k, v in class_indices.items()}
    class_names = [idx_to_class[i] for i in sorted(idx_to_class.keys())]

    # 3) classification report (text)
    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    print("\nClassification Report:\n")
    print(report)

    # save textual report to file
    report_path = os.path.join(basepath, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write("Testing Accuracy: %s\n" % B)
        f.write("Training Accuracy: %s\n\n" % C)
        f.write("Classification Report:\n")
        f.write(report)

    print(f"Saved classification report to: {report_path}")

    # 4) confusion matrix (numeric)
    cm = confusion_matrix(y_true, y_pred)
    print("\nConfusion Matrix:\n")
    print(cm)

    # save confusion matrix as image (heatmap)
    cm_fig_path = os.path.join(basepath, "confusion_matrix.png")

    try:
        plt.figure(figsize=(10, 8))
        # Use seaborn heatmap if available for nicer plot; otherwise use imshow
        try:
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                        xticklabels=class_names, yticklabels=class_names)
        except Exception:
            plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
            plt.colorbar()
            tick_marks = np.arange(len(class_names))
            plt.xticks(tick_marks, class_names, rotation=45, ha='right')
            plt.yticks(tick_marks, class_names)
            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    plt.text(j, i, format(cm[i, j], 'd'),
                             ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")

        plt.title('Confusion Matrix')
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        plt.savefig(cm_fig_path, bbox_inches='tight')
        plt.close()
        print(f"Saved confusion matrix image to: {cm_fig_path}")
    except Exception as e:
        print("Could not plot/save confusion matrix image:", str(e))

    # ---------------------------
    # Save training curves (accuracy & loss) as before
    # ---------------------------
    # summarize history for accuracy
    try:
        plt.figure()
        plt.plot(model.history['accuracy'])
        plt.plot(model.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig(basepath + "/accuracy.png", bbox_inches='tight')
        plt.close()

        # summarize history for loss
        plt.figure()
        plt.plot(model.history['loss'])
        plt.plot(model.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig(basepath + "/loss.png", bbox_inches='tight')
        plt.close()
    except Exception as e:
        print("Could not create/save training plots:", e)

    msg = B + '\n' + C + '\n\n' + "Classification report saved to: " + report_path + "\n" + "Confusion matrix image saved to: " + cm_fig_path
    return msg

# if you run as a script, call main()
if __name__ == "__main__":
    print(main())

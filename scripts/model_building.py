import tensorflow as tf

def build_keras_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(10,)),  # Input size matches the number of features
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)  # Regression output
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def run_fn(fn_args):
    # Load the data
    train_dataset = tf.data.TFRecordDataset(fn_args.train_files)
    eval_dataset = tf.data.TFRecordDataset(fn_args.eval_files)
    
    # Build the model
    model = build_keras_model()
    
    # Train the model
    model.fit(
        train_dataset.batch(32),
        validation_data=eval_dataset.batch(32),
        epochs=10
    )
    
    # Save the trained model
    model.save(fn_args.serving_model_dir, save_format='tf')
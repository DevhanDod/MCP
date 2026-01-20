"""
MLP Model for Menstrual Cycle Prediction
Extracted from CW1_w1956126_DevhanDodampahala.ipynb
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import pickle
import os

# Feature columns
NUM_COLS = ["Age", "BMI", "Stress Level", "Sleep Hours", "Cycle Length", "Period Length"]
CAT_COLS = ["Exercise Frequency", "Diet", "Symptoms"]

class MenstrualCyclePredictionModel:
    """MLP Model for predicting next menstrual cycle"""
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.model_accuracy = None
        
    def create_preprocessor(self):
        """Create the preprocessing pipeline"""
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", "passthrough", NUM_COLS),
                ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
            ]
        )
        return self.preprocessor
    
    def build_model(self, input_shape):
        """Build the MLP neural network"""
        tf.random.set_seed(42)
        
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(input_shape,)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1)  # regression output
        ])
        
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="mse",
            metrics=[tf.keras.metrics.MeanAbsoluteError(name="mae")]
        )
        
        return self.model
    
    def train(self, df):
        """Train the model on the dataset"""
        print("Preparing data...")
        
        # Filter valid data
        df = df[df["days_until_next_period"] > 0]
        
        # Prepare features and target
        X = df[NUM_COLS + CAT_COLS]
        y = df["days_until_next_period"]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"Training set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")
        
        # Create and fit preprocessor
        if self.preprocessor is None:
            self.create_preprocessor()
        
        X_train_encoded = self.preprocessor.fit_transform(X_train)
        X_test_encoded = self.preprocessor.transform(X_test)
        
        print(f"Encoded feature shape: {X_train_encoded.shape}")
        
        # Build model
        if self.model is None:
            self.build_model(X_train_encoded.shape[1])
        
        print("\nTraining model...")
        print("=" * 60)
        
        # Early stopping callback
        early_stop = tf.keras.callbacks.EarlyStopping(
            monitor="val_mae",
            patience=10,
            restore_best_weights=True
        )
        
        # Train the model
        history = self.model.fit(
            X_train_encoded, y_train,
            validation_data=(X_test_encoded, y_test),
            epochs=100,
            batch_size=64,
            callbacks=[early_stop],
            verbose=1
        )
        
        # Evaluate model
        print("\n" + "=" * 60)
        print("Evaluating model...")
        y_pred = self.model.predict(X_test_encoded, verbose=0).flatten()
        mae = np.mean(np.abs(y_test - y_pred))
        rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
        
        # Calculate accuracy (as percentage)
        self.model_accuracy = max(0, 100 - (mae / np.mean(y_test) * 100))
        
        print(f"Mean Absolute Error (MAE): {mae:.4f} days")
        print(f"Root Mean Squared Error (RMSE): {rmse:.4f} days")
        print(f"Model Accuracy: {self.model_accuracy:.2f}%")
        print("=" * 60)
        
        return history, mae, rmse
    
    def predict(self, user_input):
        """Make prediction for a single user input"""
        if self.model is None or self.preprocessor is None:
            raise ValueError("Model not trained or loaded. Please train or load a model first.")
        
        # Normalize categorical inputs
        ex = str(user_input["Exercise Frequency"]).lower().strip()
        diet = str(user_input["Diet"]).lower().strip()
        sym = str(user_input["Symptoms"]).lower().strip()
        
        # Create input dataframe
        X_one = pd.DataFrame([{
            "Age": user_input["Age"],
            "BMI": user_input["BMI"],
            "Stress Level": user_input["Stress Level"],
            "Sleep Hours": user_input["Sleep Hours"],
            "Cycle Length": user_input["Cycle Length"],
            "Period Length": user_input["Period Length"],
            "Exercise Frequency": ex,
            "Diet": diet,
            "Symptoms": sym,
        }])
        
        # Transform input
        X_one_enc = self.preprocessor.transform(X_one)
        X_one_enc = X_one_enc.toarray() if hasattr(X_one_enc, "toarray") else np.array(X_one_enc)
        
        # Make prediction
        pred_days = float(self.model.predict(X_one_enc, verbose=0).flatten()[0])
        pred_days = max(1.0, pred_days)
        
        return pred_days
    
    def save(self, model_path="saved_model", preprocessor_path="preprocessor.pkl"):
        """Save the model and preprocessor"""
        if self.model is None or self.preprocessor is None:
            raise ValueError("No model or preprocessor to save")
        
        print(f"\nSaving model to '{model_path}'...")
        self.model.save(model_path)
        
        print(f"Saving preprocessor to '{preprocessor_path}'...")
        with open(preprocessor_path, 'wb') as f:
            pickle.dump(self.preprocessor, f)
        
        # Save accuracy
        with open("model_accuracy.txt", 'w') as f:
            f.write(f"{self.model_accuracy:.2f}")
        
        print("✅ Model and preprocessor saved successfully!")
    
    def load(self, model_path="saved_model", preprocessor_path="preprocessor.pkl"):
        """Load the saved model and preprocessor"""
        print(f"Loading model from '{model_path}'...")
        self.model = tf.keras.models.load_model(model_path)
        
        print(f"Loading preprocessor from '{preprocessor_path}'...")
        with open(preprocessor_path, 'rb') as f:
            self.preprocessor = pickle.load(f)
        
        # Load accuracy
        if os.path.exists("model_accuracy.txt"):
            with open("model_accuracy.txt", 'r') as f:
                self.model_accuracy = float(f.read().strip())
        
        print("✅ Model and preprocessor loaded successfully!")
        return self

def calculate_bmi(weight_kg, height_m):
    """Calculate BMI from weight and height"""
    return weight_kg / (height_m ** 2)

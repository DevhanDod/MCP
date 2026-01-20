"""
One-time script to train and save the MLP model
Run this once to train the model, then the Flask app will load the saved model
"""

import pandas as pd
import os
import kagglehub
from model import MenstrualCyclePredictionModel

def main():
    print("="*70)
    print("🚀 MCP Model Training Script")
    print("="*70)
    print()
    
    # Download dataset
    print("📥 Downloading dataset from Kaggle...")
    try:
        path = kagglehub.dataset_download("akshayas02/menstrual-cycle-data-with-factors-dataset")
        print(f"✅ Dataset downloaded to: {path}")
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\nAlternative: If you have the CSV file, place it in the project folder")
        print("and update the path below.")
        return
    
    # Load dataset
    file_name = "menstrual_cycle_dataset_with_factors.csv"
    csv_path = os.path.join(path, file_name)
    
    print(f"\n📊 Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"✅ Dataset loaded! Shape: {df.shape}")
    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
    
    # Create and train model
    print("\n" + "="*70)
    print("🧠 Creating and training model...")
    print("="*70)
    
    model = MenstrualCyclePredictionModel()
    history, mae, rmse = model.train(df)
    
    # Save model
    print("\n" + "="*70)
    print("💾 Saving model...")
    print("="*70)
    
    model.save(
        model_path="saved_model",
        preprocessor_path="preprocessor.pkl"
    )
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETE!")
    print("="*70)
    print("\n📋 Summary:")
    print(f"   • Model saved to: saved_model/")
    print(f"   • Preprocessor saved to: preprocessor.pkl")
    print(f"   • Model accuracy: {model.model_accuracy:.2f}%")
    print(f"   • MAE: {mae:.4f} days")
    print(f"   • RMSE: {rmse:.4f} days")
    print("\n🎯 Next step: Run 'python start.py' or './run.sh' to start the app!")
    print("="*70)

if __name__ == "__main__":
    main()

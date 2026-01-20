"""
Flask Web Application for Menstrual Cycle Prediction
Uses pre-trained MLP model for instant startup
"""

from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime, timedelta
from model import MenstrualCyclePredictionModel, calculate_bmi

app = Flask(__name__)

# Global model instance
mcp_model = MenstrualCyclePredictionModel()
model_loaded = False

def load_model():
    """Load the pre-trained model"""
    global mcp_model, model_loaded
    
    print("="*60)
    print("Loading pre-trained model...")
    print("="*60)
    
    model_path = "saved_model"
    preprocessor_path = "preprocessor.pkl"
    
    # Check if model files exist
    if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
        print("❌ Model files not found!")
        print("\nPlease train the model first by running:")
        print("   python train_model.py")
        print("\nThis will download the dataset and train the model (one-time setup)")
        return False
    
    try:
        mcp_model.load(model_path, preprocessor_path)
        model_loaded = True
        print(f"✅ Model loaded successfully!")
        print(f"   Accuracy: {mcp_model.model_accuracy:.2f}%")
        print("="*60)
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/')
def index():
    """Render the input form page"""
    if not model_loaded:
        return """
        <html>
        <head><title>Model Not Found</title></head>
        <body style="font-family: Arial; padding: 40px; max-width: 800px; margin: 0 auto;">
            <h1>⚠️ Model Not Trained</h1>
            <p>The prediction model hasn't been trained yet.</p>
            <h2>Setup Instructions:</h2>
            <ol>
                <li>Stop this server (Ctrl+C)</li>
                <li>Run: <code style="background: #f0f0f0; padding: 4px 8px;">python train_model.py</code></li>
                <li>Wait for training to complete (2-5 minutes)</li>
                <li>Restart the server: <code style="background: #f0f0f0; padding: 4px 8px;">python app.py</code></li>
            </ol>
            <p><strong>This is a one-time setup!</strong> After training, the app will start instantly.</p>
        </body>
        </html>
        """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    if not model_loaded:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first.'
        }), 400
    
    try:
        data = request.json
        
        # Calculate BMI from weight and height
        weight = float(data['weight'])  # in kg
        height = float(data['height'])  # in meters
        bmi = calculate_bmi(weight, height)
        
        # Prepare user input
        user_input = {
            "Age": int(data['age']),
            "BMI": round(bmi, 2),
            "Stress Level": int(data['stress_level']),
            "Sleep Hours": float(data['sleep_hours']),
            "Cycle Length": int(data['cycle_length']),
            "Period Length": int(data['period_length']),
            "Exercise Frequency": data['exercise_frequency'],
            "Diet": data['diet'],
            "Symptoms": data['symptoms'],
        }
        
        # Make prediction
        pred_days = mcp_model.predict(user_input)
        
        # Calculate predicted date
        cycle_start = datetime.strptime(data['cycle_start_date'], "%Y-%m-%d")
        predicted_date = cycle_start + timedelta(days=pred_days)
        
        # Return results
        return jsonify({
            'success': True,
            'result': {
                'bmi': round(bmi, 2),
                'predicted_days_until_next_period': round(pred_days, 1),
                'predicted_next_cycle_start_date': predicted_date.strftime("%Y-%m-%d"),
                'accuracy': f"{mcp_model.model_accuracy:.1f}%"
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/results')
def results():
    """Render the results page"""
    return render_template('results.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'accuracy': f"{mcp_model.model_accuracy:.2f}%" if model_loaded else "N/A"
    })

if __name__ == '__main__':
    print("="*60)
    print("🚀 MCP - Menstrual Cycle Prediction Application")
    print("="*60)
    print()
    
    # Load pre-trained model
    if load_model():
        print()
        print("="*60)
        print("✨ Application ready!")
        print("="*60)
        print()
        print("🌐 Open your browser and visit:")
        print("   👉 http://localhost:5000")
        print()
        print("Press Ctrl+C to stop the server")
        print("="*60)
        print()
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print()
        print("="*60)
        print("Please train the model first!")
        print("="*60)

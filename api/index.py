from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Global model
model = None
model_accuracy = 0

def get_sample_data():
    """Generate sample menstrual cycle data for training"""
    np.random.seed(42)
    n_samples = 500
    
    data = {
        'Age': np.random.randint(18, 45, n_samples),
        'BMI': np.round(np.random.uniform(18, 35, n_samples), 1),
        'Stress Level': np.random.randint(1, 11, n_samples),
        'Sleep Hours': np.round(np.random.uniform(4, 10, n_samples), 1),
        'Cycle Length': np.random.choice([21, 24, 26, 28, 30, 32, 35], n_samples, 
                                         p=[0.05, 0.1, 0.15, 0.4, 0.15, 0.1, 0.05]),
        'Period Length': np.random.choice([3, 4, 5, 6, 7], n_samples,
                                          p=[0.1, 0.25, 0.35, 0.2, 0.1]),
        'Exercise Frequency': np.random.choice(['none', 'weekly', 'daily', 'occasionally'], n_samples,
                                               p=[0.2, 0.3, 0.25, 0.25]),
        'Diet': np.random.choice(['balanced', 'vegan', 'keto', 'irregular'], n_samples,
                                 p=[0.4, 0.2, 0.15, 0.25]),
        'Symptoms': np.random.choice(['none', 'cramps', 'headache', 'bloating', 'fatigue'], n_samples,
                                     p=[0.3, 0.25, 0.15, 0.15, 0.15])
    }
    
    base_days = data['Cycle Length'] - data['Period Length']
    variation = (data['Stress Level'] - 5) * 0.5 + (7 - data['Sleep Hours']) * 0.3
    noise = np.random.normal(0, 1, n_samples)
    data['days_until_next_period'] = np.maximum(1, base_days + variation + noise).astype(int)
    
    return pd.DataFrame(data)

def train_model():
    """Train the MLP model"""
    global model, model_accuracy
    
    df = get_sample_data()
    
    num_cols = ['Age', 'BMI', 'Stress Level', 'Sleep Hours', 'Cycle Length', 'Period Length']
    cat_cols = ['Exercise Frequency', 'Diet', 'Symptoms']
    
    X = df[num_cols + cat_cols]
    y = df['days_until_next_period']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
        ]
    )
    
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', MLPRegressor(
            hidden_layer_sizes=(32, 16),
            activation='relu',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.2
        ))
    ])
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = np.mean(np.abs(y_test - y_pred))
    model_accuracy = max(0, 100 - (mae / np.mean(y_test) * 100))
    
    return model

def predict_cycle(user_input):
    """Make prediction for user input"""
    global model
    
    X = pd.DataFrame([{
        'Age': user_input['Age'],
        'BMI': user_input['BMI'],
        'Stress Level': user_input['Stress Level'],
        'Sleep Hours': user_input['Sleep Hours'],
        'Cycle Length': user_input['Cycle Length'],
        'Period Length': user_input['Period Length'],
        'Exercise Frequency': user_input['Exercise Frequency'].lower(),
        'Diet': user_input['Diet'].lower(),
        'Symptoms': user_input['Symptoms'].lower()
    }])
    
    pred_days = float(model.predict(X)[0])
    pred_days = max(1, pred_days)
    
    return pred_days

# Train model on cold start
train_model()

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP - Menstrual Cycle Prediction</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #b8b6f3 0%, #e8d5f5 50%, #b8c5f5 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 40px;
            width: 100%;
            max-width: 900px;
        }
        .header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 30px;
        }
        .logo {
            width: 40px;
            height: 40px;
            background: #DC2626;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .logo svg { width: 24px; height: 24px; fill: white; }
        h1 { font-size: 24px; font-weight: 700; color: #1f2937; }
        .subtitle { font-size: 13px; color: #6b7280; }
        h2 { font-size: 20px; font-weight: 600; color: #1f2937; margin-bottom: 6px; }
        .form-subtitle { font-size: 14px; color: #9ca3af; margin-bottom: 25px; }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        @media (max-width: 600px) { .form-grid { grid-template-columns: 1fr; } }
        .form-group { display: flex; flex-direction: column; }
        .form-group label {
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 8px;
        }
        .required { color: #DC2626; }
        .form-group input, .form-group select {
            padding: 12px 14px;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            font-size: 14px;
            color: #1f2937;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #DC2626;
            box-shadow: 0 0 0 3px rgba(220,38,38,0.1);
        }
        .submit-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #DC2626 0%, #991b1b 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 25px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(220,38,38,0.3);
        }
        .footer {
            margin-top: 30px;
            text-align: right;
            font-size: 13px;
            color: #6b7280;
        }
        .error { background: #fee2e2; border: 1px solid #fecaca; color: #991b1b; padding: 12px; border-radius: 6px; margin-bottom: 20px; display: none; }
        .result-box { background: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 8px; margin-top: 20px; display: none; }
        .result-box h3 { color: #166534; margin-bottom: 15px; }
        .result-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #dcfce7; }
        .result-item:last-child { border-bottom: none; }
        .result-label { color: #166534; }
        .result-value { font-weight: 600; color: #15803d; }
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="logo">
                <svg viewBox="0 0 24 24"><path d="M12 2L2 7L12 12L22 7L12 2Z"/><path d="M2 17L12 22L22 17V7L12 12L2 7V17Z"/></svg>
            </div>
            <div>
                <h1>MCP</h1>
                <p class="subtitle">Menstrual Cycle Prediction</p>
            </div>
        </div>
        
        <h2>Enter Your Information</h2>
        <p class="form-subtitle">Fill in the details below to predict your next cycle</p>
        
        <div id="error" class="error"></div>
        
        <form id="form">
            <div class="form-grid">
                <div class="form-group">
                    <label>Age <span class="required">*</span></label>
                    <input type="number" id="age" required min="10" max="60" placeholder="25">
                </div>
                <div class="form-group">
                    <label>Cycle Length (days)</label>
                    <select id="cycle_length" required>
                        <option value="21">21 days</option>
                        <option value="24">24 days</option>
                        <option value="26">26 days</option>
                        <option value="28" selected>28 days</option>
                        <option value="30">30 days</option>
                        <option value="32">32 days</option>
                        <option value="35">35 days</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Weight (kg) <span class="required">*</span></label>
                    <input type="number" id="weight" required step="0.1" placeholder="55">
                </div>
                <div class="form-group">
                    <label>Exercise Frequency</label>
                    <select id="exercise" required>
                        <option value="none">None</option>
                        <option value="occasionally">Occasionally</option>
                        <option value="weekly">Weekly</option>
                        <option value="daily" selected>Daily</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Height (m) <span class="required">*</span></label>
                    <input type="number" id="height" required step="0.01" placeholder="1.65">
                </div>
                <div class="form-group">
                    <label>Symptoms</label>
                    <select id="symptoms" required>
                        <option value="none" selected>None</option>
                        <option value="cramps">Cramps</option>
                        <option value="headache">Headache</option>
                        <option value="bloating">Bloating</option>
                        <option value="fatigue">Fatigue</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Stress Level (1-10)</label>
                    <select id="stress" required>
                        <option value="1">1 - Very Low</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5" selected>5 - Medium</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                        <option value="9">9</option>
                        <option value="10">10 - Very High</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Diet</label>
                    <select id="diet" required>
                        <option value="balanced" selected>Balanced</option>
                        <option value="vegan">Vegan</option>
                        <option value="keto">Keto</option>
                        <option value="irregular">Irregular</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Period Length (days)</label>
                    <select id="period_length" required>
                        <option value="3">3 days</option>
                        <option value="4">4 days</option>
                        <option value="5" selected>5 days</option>
                        <option value="6">6 days</option>
                        <option value="7">7 days</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Sleep Hours</label>
                    <input type="number" id="sleep" required step="0.5" min="0" max="24" value="7">
                </div>
                <div class="form-group" style="grid-column: span 2;">
                    <label>Cycle Start Date <span class="required">*</span></label>
                    <input type="date" id="start_date" required>
                </div>
            </div>
            <button type="submit" class="submit-btn">Predict Next Cycle</button>
        </form>
        
        <div id="result" class="result-box">
            <h3>🎯 Prediction Results</h3>
            <div class="result-item">
                <span class="result-label">Your BMI:</span>
                <span class="result-value" id="r-bmi">--</span>
            </div>
            <div class="result-item">
                <span class="result-label">Days Until Next Period:</span>
                <span class="result-value" id="r-days">--</span>
            </div>
            <div class="result-item">
                <span class="result-label">Predicted Date:</span>
                <span class="result-value" id="r-date">--</span>
            </div>
            <div class="result-item">
                <span class="result-label">Model Accuracy:</span>
                <span class="result-value" id="r-acc">--</span>
            </div>
        </div>
        
        <div class="footer">Devhan (20221394 - w1956126)</div>
    </div>
    
    <script>
        document.getElementById('start_date').max = new Date().toISOString().split('T')[0];
        
        document.getElementById('form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.querySelector('.submit-btn');
            btn.disabled = true;
            btn.textContent = 'Processing...';
            document.getElementById('error').style.display = 'none';
            document.getElementById('result').style.display = 'none';
            
            const data = {
                age: document.getElementById('age').value,
                weight: document.getElementById('weight').value,
                height: document.getElementById('height').value,
                stress_level: document.getElementById('stress').value,
                sleep_hours: document.getElementById('sleep').value,
                cycle_length: document.getElementById('cycle_length').value,
                period_length: document.getElementById('period_length').value,
                exercise: document.getElementById('exercise').value,
                diet: document.getElementById('diet').value,
                symptoms: document.getElementById('symptoms').value,
                start_date: document.getElementById('start_date').value
            };
            
            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('r-bmi').textContent = result.result.bmi;
                    document.getElementById('r-days').textContent = result.result.days + ' days';
                    document.getElementById('r-date').textContent = result.result.next_cycle_date;
                    document.getElementById('r-acc').textContent = result.result.accuracy;
                    document.getElementById('result').style.display = 'block';
                } else {
                    document.getElementById('error').textContent = result.error;
                    document.getElementById('error').style.display = 'block';
                }
            } catch(err) {
                document.getElementById('error').textContent = 'Error: ' + err.message;
                document.getElementById('error').style.display = 'block';
            }
            
            btn.disabled = false;
            btn.textContent = 'Predict Next Cycle';
        });
    </script>
</body>
</html>'''

@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        data = request.json
        
        weight = float(data['weight'])
        height = float(data['height'])
        bmi = round(weight / (height ** 2), 2)
        
        user_input = {
            'Age': int(data['age']),
            'BMI': bmi,
            'Stress Level': int(data['stress_level']),
            'Sleep Hours': float(data['sleep_hours']),
            'Cycle Length': int(data['cycle_length']),
            'Period Length': int(data['period_length']),
            'Exercise Frequency': data['exercise'],
            'Diet': data['diet'],
            'Symptoms': data['symptoms']
        }
        
        pred_days = predict_cycle(user_input)
        
        start = datetime.strptime(data['start_date'], '%Y-%m-%d')
        next_date = start + timedelta(days=int(pred_days))
        
        return jsonify({
            'success': True,
            'result': {
                'bmi': bmi,
                'days': round(pred_days, 1),
                'next_cycle_date': next_date.strftime('%B %d, %Y'),
                'accuracy': f'{model_accuracy:.1f}%'
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

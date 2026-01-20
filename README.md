# MCP - Menstrual Cycle Prediction Application

A web-based application that uses a Multi-Layer Perceptron (MLP) neural network to predict menstrual cycle dates based on lifestyle and physiological factors.

## Features

- 🎯 **Accurate Predictions**: Uses a trained MLP model with TensorFlow
- 🎨 **Beautiful UI**: Modern, responsive interface matching high-fidelity designs
- 📊 **BMI Calculation**: Automatically calculates BMI from weight and height
- 🔒 **Privacy-Focused**: Data is processed locally, no external storage

## Project Structure

```
Project/
├── app.py                          # Flask backend application
├── requirements.txt                # Python dependencies
├── templates/
│   ├── index.html                  # Input form page
│   └── results.html                # Results display page
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       ├── script.js              # Form handling logic
│       └── results.js             # Results display logic
└── README.md                       # Documentation
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

### Input Form (First UI)

Fill in the following information:

**Personal Information:**
- **Age**: Your age (10-60 years)
- **Weight**: Your weight in kilograms (e.g., 55)
- **Height**: Your height in meters (e.g., 1.65)

**Lifestyle Factors:**
- **Stress Level**: Rate from 1-10
- **Sleep Hours**: Average hours per night (e.g., 7)
- **Exercise Frequency**: Daily, Weekly, Occasionally, or None
- **Diet**: Type of diet (e.g., balanced, vegan, etc.)

**Cycle Information:**
- **Cycle Length**: Typical cycle length in days (e.g., 28)
- **Period Length**: Typical period duration in days (e.g., 5)
- **Symptoms**: Current symptoms (Headache, Cramps, Bloating, etc.)
- **Cycle Start Date**: Date of your last cycle start

### Results Page (Second UI)

After submitting the form, you'll see:

- **Your BMI**: Calculated Body Mass Index
- **Your Next Cycle**: Predicted date for next menstrual cycle
- **Accuracy**: Model accuracy percentage

## Model Information

### Input Features

The MLP model uses the following features:

**Numerical Features:**
- Age
- BMI (calculated from weight and height)
- Stress Level (1-10)
- Sleep Hours
- Cycle Length (days)
- Period Length (days)

**Categorical Features:**
- Exercise Frequency
- Diet
- Symptoms

### Model Architecture

- **Type**: Multi-Layer Perceptron (MLP)
- **Framework**: TensorFlow/Keras
- **Architecture**:
  - Input Layer: 13 features (after one-hot encoding)
  - Hidden Layer 1: 32 neurons (ReLU activation)
  - Hidden Layer 2: 16 neurons (ReLU activation)
  - Output Layer: 1 neuron (regression output)
- **Loss Function**: Mean Squared Error (MSE)
- **Optimizer**: Adam (learning rate: 0.001)

### Dataset

- **Source**: Kaggle - Menstrual Cycle Data with Factors
- **Link**: https://www.kaggle.com/datasets/akshayas02/menstrual-cycle-data-with-factors-dataset
- **Size**: ~500 samples
- **Split**: 80% training, 20% testing

## Technical Details

### Backend (Flask)

- **Framework**: Flask 3.0.0
- **Model Loading**: Automatic training on startup
- **API Endpoints**:
  - `GET /` - Input form page
  - `POST /predict` - Prediction endpoint
  - `GET /results` - Results display page

### Frontend

- **HTML5** with semantic markup
- **CSS3** with custom styling and gradients
- **Vanilla JavaScript** for form handling
- **Responsive Design** for mobile compatibility

## Important Notes

⚠️ **Disclaimer**: This application is for educational and informational purposes only. It is NOT a medical diagnostic tool and should not be used as a substitute for professional healthcare advice.

### Limitations

- Predictions are based on statistical patterns and may not account for individual variations
- Does not model hormonal activity directly
- Accuracy depends on the quality and consistency of input data
- Not suitable for individuals with irregular cycles or specific medical conditions

## Troubleshooting

### Common Issues

1. **Module not found errors:**
   - Make sure you've activated the virtual environment
   - Run `pip install -r requirements.txt` again

2. **Port already in use:**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

3. **Dataset download fails:**
   - Check your internet connection
   - Ensure kagglehub is properly installed

4. **Model training takes too long:**
   - This is normal on first run (may take 2-5 minutes)
   - The model trains automatically when you start the app

## Credits

**Developer**: Devhan Dodampahala
- **UOW ID**: w1956126
- **IIT ID**: 20221394

**Course**: Applied Artificial Intelligence
**Institution**: University of Westminster / IIT

## License

This project is created for academic purposes as part of coursework.

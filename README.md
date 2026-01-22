# MCP - Menstrual Cycle Prediction

A web-based application that uses a Multi-Layer Perceptron (MLP) neural network to predict menstrual cycle dates based on lifestyle and physiological factors.

🌐 **Live Demo**: [https://devhandod.github.io/MCP/](https://devhandod.github.io/MCP/)

## Features

- 🧠 **AI-Powered**: Uses scikit-learn MLP neural network
- 🌐 **Runs in Browser**: No server required - uses Pyodide (Python in WebAssembly)
- 📱 **Responsive**: Works on desktop and mobile
- 🔒 **Privacy-First**: All processing happens locally in your browser

## How It Works

The application runs entirely in your browser using **Pyodide** (Python compiled to WebAssembly):

1. User visits the page
2. Pyodide loads Python runtime (~5MB)
3. scikit-learn and dependencies load (~15MB)
4. ML model trains in the browser (~3 seconds)
5. Ready to make predictions! ✅

## Input Features

**Personal Information:**
- Age (10-60 years)
- Weight (kg)
- Height (m) → BMI calculated automatically

**Lifestyle Factors:**
- Stress Level (1-10)
- Sleep Hours
- Exercise Frequency (None, Occasionally, Weekly, Daily)
- Diet (Balanced, Vegan, Keto, Irregular)

**Cycle Information:**
- Cycle Length (21-35 days)
- Period Length (3-7 days)
- Symptoms (None, Cramps, Headache, Bloating, Fatigue)
- Last Cycle Start Date

## Model Architecture

- **Type**: Multi-Layer Perceptron (MLP) Regressor
- **Framework**: scikit-learn
- **Architecture**:
  - Input Layer: 6 numerical + 3 categorical features
  - Hidden Layer 1: 32 neurons (ReLU activation)
  - Hidden Layer 2: 16 neurons (ReLU activation)
  - Output Layer: 1 neuron (days until next period)
- **Training**: 500 samples, 80/20 train/test split

## Local Development

### Prerequisites
- Python 3.9+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/DevhanDod/MCP.git
cd MCP

# Install dependencies with uv
uv sync

# For development with TensorFlow (optional)
uv sync --extra dev
```

### Run Training (Optional)

```bash
# Run the main training script
uv run python main.py
```

### Test the Web App Locally

```bash
# Start a local server
python -m http.server 8000

# Open http://localhost:8000 in your browser
```

## Project Structure

```
MCP/
├── index.html          # Static web app (Pyodide + scikit-learn)
├── main.py             # Flask app with embedded training
├── model.py            # MLP model class (TensorFlow version)
├── train_model.py      # Training script for saved model
├── CW1_*.ipynb         # Jupyter notebook with analysis
├── pyproject.toml      # Python project config (uv)
├── uv.lock             # Dependency lockfile
└── .github/workflows/  # GitHub Pages deployment
```

## Technologies

| Component | Technology |
|-----------|------------|
| ML Framework | scikit-learn (browser), TensorFlow (local) |
| Browser Runtime | Pyodide (Python in WebAssembly) |
| Frontend | Vanilla HTML/CSS/JS |
| Deployment | GitHub Pages |
| Package Manager | uv |

## Disclaimer

⚠️ This application is for **educational and informational purposes only**. It is NOT a medical diagnostic tool and should not be used as a substitute for professional healthcare advice.

### Limitations
- Predictions are based on statistical patterns
- Does not model hormonal activity directly
- Accuracy depends on input data consistency
- Not suitable for irregular cycles or medical conditions

## Credits

**Developer**: Devhan Dodampahala
- **UOW ID**: w1956126
- **IIT ID**: 20221394

**Course**: Applied Artificial Intelligence  
**Institution**: University of Westminster / IIT

## License

This project is created for academic purposes as part of coursework.

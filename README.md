# MCP - Menstrual Cycle Prediction

A web-based application that uses a Multi-Layer Perceptron (MLP) neural network to predict menstrual cycle dates based on lifestyle and physiological factors.

🌐 **Live Demo**: [https://devhandod.github.io/MCP/](https://devhandod.github.io/MCP/)

## Features

- 🧠 **AI-Powered**: MLP neural network trained on lifestyle factors
- 🌐 **Runs in Browser**: No server required - uses Pyodide (Python in WebAssembly)
- 📱 **Responsive**: Works on desktop and mobile
- 🔒 **Privacy-First**: All processing happens locally in your browser
- 📄 **Multi-Page UI**: Form and results on separate views

## How It Works

The application runs entirely in your browser using **Pyodide** (Python compiled to WebAssembly):

1. User visits the page
2. Pyodide loads Python runtime (~5MB)
3. scikit-learn and dependencies load (~15MB)
4. ML model trains in the browser (~3 seconds)
5. Ready to make predictions! ✅

## Input Features

| Category | Fields |
|----------|--------|
| **Personal** | Age, Weight (kg), Height (m) → BMI calculated |
| **Lifestyle** | Stress Level (1-10), Sleep Hours, Exercise Frequency, Diet |
| **Cycle Info** | Cycle Length, Period Length, Symptoms, Last Cycle Start Date |

## Model Architecture

```
Input Layer (6 numerical + 3 categorical features)
    ↓
Hidden Layer 1 (32 neurons, ReLU)
    ↓
Hidden Layer 2 (16 neurons, ReLU)
    ↓
Output Layer (1 neuron → days until next period)
```

- **Framework**: scikit-learn MLPRegressor
- **Training**: 500 samples, 80/20 train/test split
- **Optimization**: Adam optimizer, early stopping

## Running Locally

### Option 1: Browser Version (Static)

```bash
# Start a local server
python -m http.server 8000

# Open http://localhost:8000 in your browser
```

### Option 2: Flask Version (Full Server)

```bash
# Install dependencies with uv
uv sync

# Run the Flask app
uv run python app.py

# Open http://localhost:5000
```

### Option 3: Self-Contained Version

```bash
# Run the standalone version (trains on startup)
uv run python main.py

# Open http://localhost:5001
```

## Project Structure

```
MCP/
├── index.html              # Static web app (GitHub Pages)
├── app.py                  # Flask app with templates
├── main.py                 # Self-contained Flask app
├── model.py                # MLP model class (TensorFlow)
├── train_model.py          # Training script
├── templates/              # Flask HTML templates
│   ├── index.html
│   └── results.html
├── static/                 # CSS and JavaScript
│   ├── css/style.css
│   └── js/
├── CW1_*.ipynb            # Jupyter notebook analysis
├── pyproject.toml         # Python project config
├── uv.lock                # Dependency lockfile
└── .github/workflows/     # GitHub Pages deployment
```

## Technologies

| Component | Technology |
|-----------|------------|
| ML (Browser) | scikit-learn via Pyodide |
| ML (Local) | TensorFlow / scikit-learn |
| Browser Runtime | Pyodide (WebAssembly) |
| Web Framework | Flask (local) |
| Deployment | GitHub Pages |
| Package Manager | uv |

## Disclaimer

⚠️ **Educational purposes only**. This is NOT a medical diagnostic tool and should not replace professional healthcare advice.

### Limitations
- Predictions based on statistical patterns
- Does not model hormonal activity
- Not suitable for irregular cycles or medical conditions

## Credits

**Developer**: Devhan Dodampahala
- **UOW ID**: w1956126
- **IIT ID**: 20221394

**Course**: Applied Artificial Intelligence  
**Institution**: University of Westminster / IIT

## License

Created for academic purposes as part of coursework.

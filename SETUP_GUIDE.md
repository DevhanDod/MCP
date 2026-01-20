# 🚀 Complete Setup Guide - MCP Application

## ✨ **NEW IMPROVED VERSION!**

This version extracts the code from your Jupyter notebook and uses a **saved model** for instant startup!

---

## 📁 **Project Structure**

```
Project/
├── model.py              # ⭐ ML model code (from notebook)
├── train_model.py        # ⭐ One-time training script
├── app.py                # ⭐ Flask web app (loads saved model)
├── start.py              # ⭐ Easy startup script
│
├── templates/            # HTML files
│   ├── index.html        # Input form UI
│   └── results.html      # Results display UI
│
├── static/               # CSS & JavaScript
│   ├── css/style.css
│   └── js/
│       ├── script.js
│       └── results.js
│
├── saved_model/          # 📦 Trained model (created after training)
├── preprocessor.pkl      # 📦 Data preprocessor (created after training)
├── model_accuracy.txt    # 📦 Model accuracy (created after training)
│
└── requirements.txt      # Dependencies
```

---

## 🎯 **Quick Start (3 Steps)**

### **Step 1: Setup (One-time)**

```bash
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Train Model (One-time, 2-5 minutes)**

```bash
python train_model.py
```

This will:
- ✅ Download dataset from Kaggle
- ✅ Train the MLP model
- ✅ Save model to `saved_model/`
- ✅ Save preprocessor to `preprocessor.pkl`

**You only do this ONCE!** ⏰

### **Step 3: Run the App (Every time)**

```bash
python start.py
```

Or simply:

```bash
source venv/bin/activate
python app.py
```

Then open: **http://localhost:5000** 🌐

---

## 🔄 **How It Works Now**

### **Old Way (Slow):**
```
Start App → Download Dataset → Train Model (5 min) → Run App
EVERY TIME!
```

### **New Way (Fast!):**
```
First time: Train Model (5 min) → Save Model
Every other time: Load Model (2 sec) → Run App ⚡
```

---

## 📚 **What Each File Does**

| File | Purpose | When to Use |
|------|---------|-------------|
| `model.py` | ML model class (from your notebook) | Core logic |
| `train_model.py` | Train and save model | **Once** |
| `app.py` | Flask web server | Every time |
| `start.py` | Smart startup script | Easiest way |

---

## 🎓 **Understanding the Code**

### **model.py** - Extracted from Notebook

Contains the exact code from your notebook:
- Feature engineering
- Preprocessing pipeline  
- MLP architecture (32 → 16 → 1)
- Training logic
- Prediction function

### **train_model.py** - One-Time Setup

```python
# Downloads dataset
# Trains model
# Saves everything for later use
```

### **app.py** - Web Server

```python
# Loads saved model (instant!)
# Handles web requests
# Returns predictions
```

---

## 💻 **Usage Examples**

### **First Time:**

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Train (one-time)
python train_model.py

# Run
python start.py
```

### **Every Other Time:**

```bash
# Just activate and run!
source venv/bin/activate
python start.py
```

That's it! Takes 2 seconds to start! ⚡

---

## 🛠️ **Troubleshooting**

### **Problem: ModuleNotFoundError**

**Solution:** Activate virtual environment
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your prompt.

---

### **Problem: Model files not found**

**Solution:** Train the model first
```bash
python train_model.py
```

---

### **Problem: Port 5000 already in use**

**Solution:** Kill the existing process
```bash
lsof -ti:5000 | xargs kill -9
```

---

### **Problem: Training fails**

**Possible causes:**
1. No internet connection (needs to download dataset)
2. Insufficient disk space
3. Kaggle API issues

**Solution:** Check error messages, ensure internet connection

---

## 🔧 **Advanced**

### **Retrain the Model**

If you want to retrain with new data:

```bash
python train_model.py
```

This will overwrite the existing saved model.

### **Check Model Info**

```bash
cat model_accuracy.txt
```

### **Test the Model Directly**

```python
from model import MenstrualCyclePredictionModel, calculate_bmi

# Load model
model = MenstrualCyclePredictionModel()
model.load()

# Make prediction
user_data = {
    "Age": 25,
    "BMI": 22.5,
    "Stress Level": 5,
    "Sleep Hours": 7,
    "Cycle Length": 28,
    "Period Length": 5,
    "Exercise Frequency": "daily",
    "Diet": "balanced",
    "Symptoms": "none"
}

days = model.predict(user_data)
print(f"Predicted days until next period: {days:.1f}")
```

---

## ✅ **Benefits of This Approach**

1. **⚡ Instant Startup** - No waiting for training
2. **🎯 Clean Code** - Separated concerns (ML vs Web)
3. **📦 Portable** - Share `saved_model/` folder, no retraining needed
4. **🔄 Reusable** - Model code extracted from notebook
5. **🚀 Production-Ready** - Professional structure

---

## 📝 **Summary**

**Old approach:**
- Train every time app starts (5 min wait) 😴
- Messy code in one file
- Slow development cycle

**New approach:**
- Train once, use forever ⚡
- Clean, professional structure 
- Instant startup (2 seconds)
- Code from your notebook!

---

## 🎉 **You're All Set!**

Now you have a professional Flask app using the ML model from your coursework notebook!

Questions? Check the main `README.md` or the code comments.

**Happy predicting! 🔮**

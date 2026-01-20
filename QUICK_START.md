# 🚀 Quick Start Guide

## Two Ways to Run the Application

### **Method 1: Simple (Recommended)**

```bash
# Open Terminal in the project folder and run:
source venv/bin/activate
python start.py
```

That's it! The app will:
- ✅ Check all dependencies
- ✅ Show clear error messages if something is wrong
- ✅ Download dataset and train model
- ✅ Start the server

### **Method 2: Using the Shell Script**

```bash
./run.sh
```

---

## ✅ First Time Setup (One-time only)

```bash
# 1. Navigate to project
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"

# 2. Create virtual environment (only once!)
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies (only once!)
pip install -r requirements.txt
```

---

## 🎯 After First Setup

Every time you want to run the app:

```bash
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"
source venv/bin/activate
python start.py
```

**Or just:**

```bash
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"
./run.sh
```

---

## 🌐 Access the Application

Once running, open your browser:

```
http://localhost:5000
```

---

## ❓ Troubleshooting

### **Issue: "No module named 'flask'"**

**Solution:** You forgot to activate the virtual environment
```bash
source venv/bin/activate
```
You should see `(venv)` at the start of your terminal prompt.

---

### **Issue: "Port already in use"**

**Solution:** Another instance is running. Kill it:
```bash
lsof -ti:5000 | xargs kill -9
```

---

### **Issue: App stops immediately**

**Solution:** Run with the new start.py script to see errors:
```bash
python start.py
```

---

### **Issue: Model training fails**

**Possible causes:**
1. No internet connection
2. Kaggle API issues
3. Insufficient disk space

**Solution:** Check error messages - the new start.py shows detailed errors

---

## 📝 Development Tips

**Don't need to reinstall dependencies every time!**

The dependencies are saved in the `venv` folder. You only install once.

After that, just:
1. Activate venv: `source venv/bin/activate`
2. Run app: `python start.py`

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal where the app is running.

---

## 📧 Need Help?

Check the main README.md for detailed documentation.

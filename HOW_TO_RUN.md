# 🚀 HOW TO RUN - Simple Instructions

## ✨ **FIRST TIME ONLY** (One-time setup)

### Step 1: Train the Model

```bash
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"
source venv/bin/activate
python train_model.py
```

Wait 2-5 minutes while it:
- Downloads the dataset
- Trains the MLP model
- Saves everything

**You only do this ONCE!** ✅

---

## 🎯 **EVERY TIME YOU WANT TO RUN THE APP**

### Option 1: Super Simple

```bash
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"
source venv/bin/activate
python start.py
```

### Option 2: Direct

```bash
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"
source venv/bin/activate
python app.py
```

### Option 3: Shell Script

```bash
cd "/Users/devhandodampahala/Desktop/Level 6/applied ai /CW/Project"
./run.sh
```

---

## 🌐 **Access the App**

Open your browser and go to:

```
http://localhost:5000
```

---

## ⚡ **Why This is Better**

### **Before:**
- App starts → Downloads dataset → Trains model (5 min) → Ready
- **EVERY. SINGLE. TIME.** 😫

### **Now:**
- First time: Train model (5 min) ✅
- Every other time: Start app (2 seconds) ⚡

---

## 📋 **Summary**

1. **First time:** Run `python train_model.py` (one-time, 5 min)
2. **Every other time:** Run `python start.py` (instant!)
3. **Open browser:** http://localhost:5000

**That's it!** 🎉

---

## ❓ **Having Issues?**

### Dependencies not installed?
```bash
pip install -r requirements.txt
```

### Model not found?
```bash
python train_model.py
```

### Port already in use?
```bash
lsof -ti:5000 | xargs kill -9
```

---

## 📚 **More Info**

- **Detailed Setup:** See `SETUP_GUIDE.md`
- **Full Documentation:** See `README.md`
- **Quick Reference:** See `QUICK_START.md`

# 🥗 NutriMeal — Personalized Daily Meal Planner

A desktop application that generates a personalized full-day meal plan based on your body stats and fitness goals using **Machine Learning (K-Means Clustering)** and a real Indian food nutrition dataset.

---

## 📸 Features

- Calculates your daily calorie & protein targets using the **Mifflin-St Jeor TDEE formula**
- Uses **K-Means Clustering** to group foods by nutritional profile
- Recommends 3 meals (Breakfast, Lunch, Dinner) tailored to your goal
- Supports **Veg / Non-Veg** diet types
- Tracks daily calorie and protein totals with a gap warning
- Clean **dark-mode desktop UI** built with CustomTkinter
- No food repeats across meals in the same day

---

## 🗂️ Project Structure

```
Nutrimeal/
├── data/
│   └── data.csv              # Indian food nutrition dataset
├── model/
│   └── model.py              # K-Means clustering logic
├── src/
│   ├── loaddata.py           # Data loading & cleaning
│   ├── nutrition.py          # TDEE & protein calculator
│   └── meal_generator.py     # Meal recommendation engine
├── app.py                    # Desktop UI (CustomTkinter)
├── main.py                   # CLI entry point (for testing)
└── requirements.txt          # Python dependencies
```

---

## ⚙️ Installation

### 1. Clone or copy the project

```bash
cd Nutrimeal
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the desktop app

```bash
python app.py
```

Or test via CLI:

```bash
python main.py
```

---

## 📦 Requirements

```
customtkinter
pandas
scikit-learn
numpy
```

> Python 3.8 or higher required.

---

## 🧠 How It Works

### Step 1 — Data Cleaning (`src/loaddata.py`)
Loads the CSV dataset and removes beverages, condiments, desserts, spice blends, and mislabeled items to keep only real meal foods.

### Step 2 — K-Means Clustering (`model/model.py`)
Groups all foods into 4 clusters based on Calories, Protein, Carbs, and Fat:

| Cluster | Profile | Used for |
|---------|---------|----------|
| Light | ~90 kcal | Excluded from main meals |
| Balanced | ~218 kcal | All goals |
| High Carb | ~402 kcal | Muscle gain |
| High Fat | ~675 kcal | Always excluded |

### Step 3 — TDEE Calculation (`src/nutrition.py`)
Uses the Mifflin-St Jeor formula multiplied by an activity factor to calculate your daily calorie needs, then adjusts for goal:

- **Muscle gain** → TDEE + 300 kcal
- **Fat loss** → TDEE − 300 kcal
- **Maintain** → TDEE

### Step 4 — Meal Generation (`src/meal_generator.py`)
Splits daily targets across 3 meals (25% / 40% / 35%), picks foods from the correct cluster, ensures no food repeats across meals, and calculates serving quantities.

---

## 🎯 Supported Goals

| Goal | Calorie Adjustment | Protein Target |
|------|--------------------|----------------|
| Muscle gain | +300 kcal | 2.0g per kg |
| Fat loss | −300 kcal | 1.6g per kg |
| Maintain | No change | 1.2g per kg |

---

## ⚠️ Known Limitation

This dataset is Indian food-focused and carb-heavy by nature. For high muscle-gain protein targets (e.g. 160g/day), a ~10–20g protein gap may remain. The app will warn you and suggest supplements like paneer, eggs, or a protein shake to close the gap.

---

## 👨‍💻 Built With

- [Python 3](https://www.python.org/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [scikit-learn](https://scikit-learn.org/)
- [pandas](https://pandas.pydata.org/)
- [Kaggle — Indian Food Nutrition Dataset](https://www.kaggle.com/)
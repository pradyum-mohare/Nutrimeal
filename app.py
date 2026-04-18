import customtkinter as ctk
from src.loaddata import loaddata
from src.nutrition import calculate_calories, calculate_protein
from src.meal_generator import generate_full_day_plan
from model.model import apply_kmeans

# Load & cluster data once at startup
df = loaddata("data/data.csv")
df = apply_kmeans(df)

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("NutriMeal — Meal Planner")
app.geometry("720x850")
app.resizable(False, False)

# ── Title ──────────────────────────────────────────────
ctk.CTkLabel(app, text="🥗 NutriMeal", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(24, 4))
ctk.CTkLabel(app, text="Personalized daily meal planner", font=ctk.CTkFont(size=13),
             text_color="gray").pack(pady=(0, 16))

# ── Input Form ─────────────────────────────────────────
form = ctk.CTkFrame(app, corner_radius=12)
form.pack(padx=32, fill="x")

def row(parent, label, row_n):
    ctk.CTkLabel(parent, text=label, width=120, anchor="w").grid(
        row=row_n, column=0, padx=16, pady=8, sticky="w")

# Age
row(form, "Age", 0)
age_var = ctk.StringVar(value="20")
ctk.CTkEntry(form, textvariable=age_var, width=200).grid(row=0, column=1, padx=8, pady=8)

# Weight
row(form, "Weight (kg)", 1)
weight_var = ctk.StringVar(value="70")
ctk.CTkEntry(form, textvariable=weight_var, width=200).grid(row=1, column=1, padx=8, pady=8)

# Height
row(form, "Height (cm)", 2)
height_var = ctk.StringVar(value="170")
ctk.CTkEntry(form, textvariable=height_var, width=200).grid(row=2, column=1, padx=8, pady=8)

# Gender
row(form, "Gender", 3)
gender_var = ctk.StringVar(value="male")
ctk.CTkOptionMenu(form, variable=gender_var, values=["male", "female"], width=200).grid(
    row=3, column=1, padx=8, pady=8)

# Activity
row(form, "Activity", 4)
activity_var = ctk.StringVar(value="moderate")
ctk.CTkOptionMenu(form, variable=activity_var,
                  values=["sedentary", "light", "moderate", "active", "very_active"],
                  width=200).grid(row=4, column=1, padx=8, pady=8)

# Goal
row(form, "Goal", 5)
goal_var = ctk.StringVar(value="muscle")
ctk.CTkOptionMenu(form, variable=goal_var,
                  values=["muscle", "fat_loss"],
                  width=200).grid(row=5, column=1, padx=8, pady=8)

# Diet
row(form, "Diet", 6)
diet_var = ctk.StringVar(value="Veg")
ctk.CTkOptionMenu(form, variable=diet_var,
                  values=["Veg", "Non-Veg"],
                  width=200).grid(row=6, column=1, padx=8, pady=8)

# ── Result Area ────────────────────────────────────────
result_box = ctk.CTkTextbox(app, height=260, corner_radius=12,
                             font=ctk.CTkFont(family="Courier", size=13))
result_box.pack(padx=32, pady=16, fill="x")
result_box.insert("end", "Fill in your details and click Generate ↓")
result_box.configure(state="disabled")

# ── Status label ───────────────────────────────────────
status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=12), text_color="gray")
status_label.pack()

# ── Generate Function ──────────────────────────────────
def generate():
    try:
        age    = int(age_var.get())
        weight = float(weight_var.get())
        height = float(height_var.get())
    except ValueError:
        status_label.configure(text="⚠️  Please enter valid numbers.", text_color="orange")
        return

    gender   = gender_var.get()
    activity = activity_var.get()
    goal     = goal_var.get()
    diet     = diet_var.get()

    cal     = calculate_calories(weight, height, age, gender, goal, activity)
    protein = calculate_protein(weight, goal)

    plan    = generate_full_day_plan(df, diet, cal, protein, goal)
    totals  = plan.pop("_totals")

    lines = []
    lines.append(f"  Target: {cal} kcal  |  {protein:.0f}g protein")
    lines.append("  " + "─" * 44)

    icons = {"Breakfast": "🌅", "Lunch": "☀️", "Dinner": "🌙"}

    for meal, result in plan.items():
        icon = icons.get(meal, "🍽️")
        lines.append(f"\n  {icon}  {meal}  —  {result['calories']} kcal | {result['protein']}g protein")
        for item in result["items"]:
            lines.append(f"      •  {item}")

    lines.append("\n  " + "═" * 44)
    lines.append(f"  Day total :  {totals['calories']} kcal  (target: {totals['target_cal']})")
    lines.append(f"  Protein   :  {totals['protein']}g  (target: {totals['target_protein']:.0f}g)")

    gap = totals['target_protein'] - totals['protein']
    if gap > 10:
        lines.append(f"\n  ⚠️  Protein gap: {gap:.0f}g")
        lines.append("  Tip: add paneer, eggs, or a protein shake.")

    output = "\n".join(lines)

    result_box.configure(state="normal")
    result_box.delete("1.0", "end")
    result_box.insert("end", output)
    result_box.configure(state="disabled")

    status_label.configure(text="✅  Meal plan generated!", text_color="green")

# ── Generate Button ────────────────────────────────────
ctk.CTkButton(app, text="Generate Meal Plan", height=44,
              font=ctk.CTkFont(size=15, weight="bold"),
              command=generate).pack(padx=32, pady=(0, 8), fill="x")

app.mainloop()
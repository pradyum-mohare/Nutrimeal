from src.loaddata import loaddata
from src.nutrition import calculate_calories, calculate_protein
from src.meal_generator import generate_full_day_plan
from model.model import apply_kmeans

df = loaddata("data/data.csv")
df = apply_kmeans(df)

gender   = "male"
weight   = 70
height   = 174
age      = 20
goal     = "muscle"
activity = "moderate"

cal     = calculate_calories(weight, height, age, gender, goal, activity)
protein = calculate_protein(weight, goal)

print(f"\nTarget: {cal} kcal | {protein:.0f}g protein")
print("-" * 40)

plan = generate_full_day_plan(df, "Veg", cal, protein, goal)
totals = plan.pop("_totals")

for meal, result in plan.items():
    print(f"\n{meal}:  ({result['calories']} kcal | {result['protein']}g protein)")
    for item in result["items"]:
        print("  -", item)

print("\n" + "=" * 40)
print(f"Day total:  {totals['calories']} kcal  (target: {totals['target_cal']})")
print(f"Protein:    {totals['protein']}g  (target: {totals['target_protein']:.0f}g)")

gap = totals['target_protein'] - totals['protein']
if gap > 10:
    print(f"\n⚠️  Protein gap: {gap:.0f}g — this dataset is carb-heavy.")
    print("   Tip: add eggs, paneer, Greek yogurt, or a protein shake to close the gap.")
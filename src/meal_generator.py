MEAL_CAL_CAPS = {
    "Breakfast": 600,
    "Lunch":     900,
    "Dinner":    800,
    "Anytime":   600
}

def filter_by_cluster(df, goal):
    df = df[df['Cluster_Name'] != 'High Fat']
    if goal == "fat_loss":
        df = df[df['Cluster_Name'].isin(['Light', 'Balanced'])]
    elif goal == "muscle":
        df = df[df['Cluster_Name'].isin(['Balanced', 'High Carb'])]
    else:
        df = df[df['Cluster_Name'].isin(['Light', 'Balanced', 'High Carb'])]
    return df


def generate_meal(df, meal_type, diet_type, target_cal, target_protein, goal, used_foods=None):
    if used_foods is None:
        used_foods = set()

    df = filter_by_cluster(df, goal)

    if diet_type.lower() == "veg":
        df = df[df['Type'].str.lower() == "veg"]

    df = df[(df['Meal'] == meal_type) | (df['Meal'] == 'Anytime')]

    cal_cap = MEAL_CAL_CAPS.get(meal_type, 700)
    df = df[(df['Calories'] > 80) & (df['Calories'] <= cal_cap)]

    # Exclude foods already used in earlier meals
    df = df[~df['Food'].isin(used_foods)]

    if df.empty:
        return {"items": ["No food available for this meal"], "calories": 0, "protein": 0}

    staple_df = df[df['Category'] == 'Staple']
    variety_df = df[df['Category'] == 'Variety']

    foods = []

    # Pick up to 2 staples
    n_staples = min(2, len(staple_df))
    if n_staples > 0:
        foods.extend(staple_df.sample(n_staples, replace=False).to_dict('records'))

    # Pick 1 variety — always pick highest protein available
    if not variety_df.empty:
        pool = variety_df[~variety_df['Food'].isin([f['Food'] for f in foods])]
        if not pool.empty:
            best = pool.nlargest(3, 'Protein').sample(1).to_dict('records')[0]
            foods.append(best)

    # Guarantee minimum 3 foods
    if len(foods) < 3:
        already = set(f['Food'] for f in foods)
        extra = df[~df['Food'].isin(already)].nlargest(10, 'Protein')
        needed = 3 - len(foods)
        if len(extra) >= needed:
            foods.extend(extra.sample(needed).to_dict('records'))

    if not foods:
        return {"items": ["No food available for this meal"], "calories": 0, "protein": 0}

    # Qty: calories drive the quantity, protein is tracked
    total_food_cal     = sum(f['Calories'] for f in foods)
    total_food_protein = sum(f['Protein']  for f in foods)

    qty_for_cal = target_cal / total_food_cal if total_food_cal > 0 else 1
    qty = max(1, round(qty_for_cal))

    actual_cal     = round(total_food_cal     * qty)
    actual_protein = round(total_food_protein * qty, 1)

    items = [f"{row['Food']} (x{qty})" for row in foods]

    return {
        "items":    items,
        "calories": actual_cal,
        "protein":  actual_protein
    }


def generate_full_day_plan(df, diet_type, total_cal, total_protein, goal):
    meal_plan = [
        ("Breakfast", 0.25),
        ("Lunch",     0.40),
        ("Dinner",    0.35),
    ]

    plan = {}
    used_foods  = set()
    day_cal     = 0
    day_protein = 0

    for meal_label, ratio in meal_plan:
        meal_cal     = int(total_cal * ratio)
        meal_protein = total_protein * ratio

        result = generate_meal(
            df, meal_label, diet_type, meal_cal, meal_protein, goal, used_foods
        )

        for item in result["items"]:
            food_name = item.split(" (x")[0]
            used_foods.add(food_name)

        day_cal     += result["calories"]
        day_protein += result["protein"]

        plan[meal_label] = result

    # Daily totals
    plan["_totals"] = {
        "calories":       day_cal,
        "protein":        round(day_protein, 1),
        "target_cal":     total_cal,
        "target_protein": total_protein
    }

    return plan
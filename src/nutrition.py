ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}

def calculate_bmi(weight_kg, height_cm):
    return weight_kg / ((height_cm / 100) ** 2)

def calculate_calories(weight, height, age, gender, goal, activity):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Apply activity multiplier (this was missing!)
    tdee = bmr * ACTIVITY_MULTIPLIERS.get(activity, 1.55)

    if goal == "muscle":
        return int(tdee + 300)
    elif goal == "fat_loss":
        return int(tdee - 300)
    else:
        return int(tdee)

def calculate_protein(weight, goal):
    if goal == "muscle":
        return weight * 2.0
    elif goal == "fat_loss":
        return weight * 1.6
    else:
        return weight * 1.2
    

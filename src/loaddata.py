import pandas as pd

def loaddata(path):
    df = pd.read_csv(path)

    df = df.rename(columns={
        'Dish Name':           'Food',
        'Calories (kcal)':     'Calories',
        'Protein (g)':         'Protein',
        'Carbohydrates (g)':   'Carbs',
        'Fats (g)':            'Fat',
        'Meal Category':       'Meal',
        'Diet Type':           'Type',
        'Frequency':           'Category'
    })

    df['Category'] = df['Category'].replace({'Non-Staple': 'Variety'})
    df['Food'] = df['Food'].str.strip().str.lower()

    # Beverages & drinks
    df = df[~df['Food'].str.contains(
        'tea|coffee|drink|juice|beverage|milkshake|lassi|cooler|lemonade|'
        'sherbet|squash|punch|cocoa|nog|masala',
        case=False
    )]

    # Soups
    df = df[~df['Food'].str.contains('soup|broth', case=False)]

    # Condiments, dressings, seasonings
    df = df[~df['Food'].str.contains(
        'pickle|achar|chutney|sauce|dressing|mayonnaise|icing|baghar|tadka|raita',
        case=False
    )]

    # Desserts & sweets
    df = df[~df['Food'].str.contains(
        'cookie|biscuit|cake|halwa|ladoo|burfi|chocolate|pastry|sweet|'
        'gulab jamun|gunjia|ghujia|malpua|mal pua|barfi|mithai|kheer|'
        'pudding|custard|mousse|trifle|fudge|brownie|souffle|'
        'cream horn|melting moment|danish|shortbread',
        case=False
    )]

    # Fried snack foods
    df = df[~df['Food'].str.contains(
        'chips|bhujia|sev|murukku|chakli|papdi|chikki|bhel|chaat|puff|'
        'cracker|popcorn|farsan|khakhra|namak para',
        case=False
    )]

    # Known mislabeled non-veg items in dataset
    df = df[~df['Food'].str.contains(
        'roghan josh|rogan josh',
        case=False
    )]

    # Infant / misc
    df = df[~df['Food'].str.contains('infant|baby|snack', case=False)]

    # Remove very light items
    df = df[df['Calories'] > 100]

    return df
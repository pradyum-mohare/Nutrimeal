from sklearn.cluster import KMeans
import numpy as np

def apply_kmeans(df):
    X = df[['Calories', 'Protein', 'Carbs', 'Fat']]
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X)
    
 
    centers = kmeans.cluster_centers_
    calorie_order = np.argsort(centers[:, 0]) 
    
    rank_map = {old: new for new, old in enumerate(calorie_order)}
    df['Cluster'] = df['Cluster'].map(rank_map)
    
    
    CLUSTER_MAP = {
        0: "Low Calorie",
        1: "Balanced",
        2: "High Protein",
        3: "High Carb"
    }
    df['Cluster_Name'] = df['Cluster'].map(CLUSTER_MAP)
    
    return df
"""
EV Charging Station Clustering - Radius Optimization

This script downloads EV charging station data from Kaggle using kagglehub,
finds the optimal geographic radius to group stations into balanced clusters (shards),
and outputs an interactive map showing the results.

Original dataset: https://www.kaggle.com/datasets/venkatsairo4899/ev-charging-station-usage-of-california-city
"""

# Install dependencies if needed:
# pip install kagglehub haversine folium scikit-learn pandas

import kagglehub
import pandas as pd
import os
import numpy as np
from haversine import haversine, Unit
import folium

# Download dataset from Kaggle via kagglehub
path = kagglehub.dataset_download("venkatsairo4899/ev-charging-station-usage-of-california-city")
print("📥 Dataset downloaded to:", path)

# Read CSV file
csv_path = os.path.join(path, "EVChargingStationUsage.csv")
df = pd.read_csv(csv_path)

# Extract unique locations (latitude and longitude)
unique_locations = df[['Latitude', 'Longitude']].dropna().drop_duplicates()
locations = unique_locations.values
print(f"📍 Number of unique charging stations: {len(locations)}")


# Function to optimize the clustering radius
def optimize_radius(locations, initial_radius=0.1, max_radius=2.0, step=0.01):
    best_result = None
    best_std = float('inf')
    radius_km = initial_radius

    # Clustering function: creates shards based on a radius
    def create_shards(radius):
        used = set()
        shards = []

        def count_neighbors(point):
            return sum(1 for j, other in enumerate(locations)
                       if j not in used and haversine(point, other) <= radius)

        while len(used) < len(locations):
            best_idx, best_score = -1, -1
            for i, point in enumerate(locations):
                if i in used:
                    continue
                score = count_neighbors(point)
                if score > best_score:
                    best_score = score
                    best_idx = i

            center = locations[best_idx]
            shard = []
            for j, other in enumerate(locations):
                if j not in used and haversine(center, other) <= radius:
                    shard.append(j)
                    used.add(j)
            shards.append(shard)

        return shards

    # Try increasing radii to find the best configuration
    while radius_km <= max_radius:
        shards = create_shards(radius_km)
        sizes = [len(s) for s in shards]
        avg_size = np.mean(sizes)
        std_dev = np.std(sizes)

        if 4 <= avg_size <= 20 and std_dev <= 2.5:
            print(f"✅ Optimal radius found: {radius_km:.3f} km")
            print(f"Shards: {len(shards)}, Avg Size: {avg_size:.2f}, Std Dev: {std_dev:.2f}")
            return radius_km, shards

        if std_dev < best_std:
            best_std = std_dev
            best_result = (radius_km, shards, avg_size, std_dev)

        radius_km += step

    # Return best result if constraints weren't fully met
    print(f"✔️ Best fallback radius: {best_result[0]:.3f} km")
    print(f"Shards: {len(best_result[1])}, Avg Size: {best_result[2]:.2f}, Std Dev: {best_result[3]:.2f}")
    return best_result[0], best_result[1]


# Run optimization
optimal_radius, final_shards = optimize_radius(locations)

# Calculate map center
center_lat = np.mean([loc[0] for loc in locations])
center_lon = np.mean([loc[1] for loc in locations])

# Create Folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Draw stations and cluster boundaries
for shard in final_shards:
    center_point = locations[shard[0]]  # Take first point in shard as center
    for idx in shard:
        folium.CircleMarker(
            location=locations[idx],
            radius=2,
            color='blue',
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    folium.Circle(
        location=center_point,
        radius=optimal_radius * 1000,  # km to meters
        color='green',
        fill=False
    ).add_to(m)

# Save interactive map
output_path = "optimized_radius_shards_map.html"
m.save(output_path)
print(f"🗺️ Map saved as {output_path}")

# ⚡ EV Charging Station Clustering (California City)

This project clusters electric vehicle (EV) charging stations in California City using a radius-based sharding algorithm. By calculating real-world distances (via the Haversine formula), it identifies the optimal radius to group stations into compact and balanced clusters. The results are visualized on an interactive map.

---

## 🔍 What’s the Goal?

Efficient EV charging infrastructure depends on smart location planning. Instead of using fixed-size grids or k-means clustering, this project:

- Dynamically determines the best grouping radius
- Ensures clusters are balanced (by average size and standard deviation)
- Uses **geographic distance**, not Euclidean
- Generates an interactive map to visualize clusters

---

## 📦 Dataset

We use the real-world dataset from Kaggle:

🔗 [EV Charging Station Usage of California City](https://www.kaggle.com/datasets/venkatsairo4899/ev-charging-station-usage-of-california-city)

It contains:
- Latitude / Longitude of stations
- Station metadata and usage info

---

## 🧠 Features of this Project

- Automatically downloads dataset using `kagglehub`
- Extracts unique station locations
- Optimizes radius for shard formation (with constraints)
- Implements custom greedy clustering algorithm
- Visualizes clusters using `folium`
- Outputs interactive HTML map

---

## 🛠 Requirements

- Python 3.7+
- Libraries:
  - `pandas`
  - `numpy`
  - `folium`
  - `haversine`
  - `scikit-learn`
  - `kagglehub`

Install them all at once:

```bash
pip install kagglehub haversine folium scikit-learn pandas

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

# Sample list of vectors (replace with your actual data)
data_ = pd.read_csv('new/belief_embedding.csv')

# Select features (data points) and labels (optional)
X = data_.iloc[:, 1:]  # Assuming features start from the second column
labels = data_.iloc[:, 0]  # Extract labels from the first column (optional)

k_range = range(2, 40)
j = 0
result = []
while True:
# Calculate silhouette scores for each n_clusters
  silhouette_scores_ = []
  for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    silhouette_scores_.append(silhouette_score(X, kmeans.labels_))

  # Find the k with the highest average silhouette score
  best_k = k_range[silhouette_scores_.index(max(silhouette_scores_))]
  print("Estimated optimal number of clusters:", best_k)

  print(result)
  result = result + [best_k]
  j += 1
  if j >= 10:
      break

print("best_ks:", result)




from sklearn.cluster import KMeans
from sklearn.decomposition import PCA  # For dimensionality reduction (if needed)
import matplotlib.pyplot as plt
import pandas as pd

# Replace 'your_data.csv' with the actual path to your file
data = pd.read_csv('new/belief_embedding.csv')

# Select features (data points) and labels (optional)
X = data.iloc[:, 1:]  # Assuming features start from the second column
print(X)
labels = data.iloc[:, 0]  # Extract labels from the first column (optional)


# Choose the number of clusters (adjust as needed)
n_clusters = 5

# Perform clustering using KMeans
kmeans = KMeans(n_clusters=38)
kmeans.fit(X)

# Reduce dimensionality to 2D for visualization (if necessary)
if X.shape[1] > 2:
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
else:
    X_pca = X

# Get cluster labels
cluster_labels = kmeans.labels_

# Create a DataFrame to store labels and data points
df = pd.DataFrame({"Data Point": data.values.tolist(), "Cluster": cluster_labels})

# Save the DataFrame as a CSV file
# df.to_csv("new/belief_embedding_kmeans_results.csv", index=False)

# Visualize the clusters using scatter plot
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels)  # Adjust columns for 2D data

# Add labels and title
plt.xlabel(" ")
plt.ylabel(" ")
plt.title("Belief Embedding Clustering (KMeans)")
plt.show()



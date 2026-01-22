"""
K-Means Clustering for Learning Pattern Analysis

This module implements K-Means clustering to group students by learning behaviors
and patterns, enabling personalized insights and recommendations.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt


class LearningPatternClusterer:
    """
    Clusters students based on learning patterns using K-Means algorithm.

    Features analyzed:
    - Study duration patterns
    - Time of day preferences
    - Subject diversity
    - Resource usage patterns
    - Collaboration frequency
    - Productivity scores
    """

    def __init__(self, n_clusters: int = None, random_state: int = 42):
        """
        Initialize clusterer.

        Args:
            n_clusters: Number of clusters. If None, will be determined automatically.
            random_state: Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = None
        self.feature_names = []
        self.cluster_profiles = {}

    def extract_features(self, learning_patterns: List[Dict]) -> np.ndarray:
        """
        Extract numerical features from learning pattern data.

        Args:
            learning_patterns: List of learning pattern records

        Returns:
            Feature matrix (n_samples, n_features)
        """
        features = []
        self.feature_names = [
            'avg_study_duration',
            'peak_hour',
            'session_count',
            'subject_diversity',
            'collaboration_ratio',
            'productivity_score',
            'consistency_score',
            'morning_ratio',
            'afternoon_ratio',
            'evening_ratio',
            'night_ratio',
            'resource_diversity'
        ]

        for pattern in learning_patterns:
            feature_vector = [
                pattern.get('total_study_duration', 0) / 60,  # Convert to hours
                pattern.get('peak_productivity_hour', 12),
                pattern.get('session_count', 0),
                self._calculate_subject_diversity(pattern.get('subjects_studied', [])),
                self._calculate_collaboration_ratio(pattern),
                pattern.get('productivity_score', 5.0),
                pattern.get('consistency_score', 5.0),
                self._calculate_time_ratio(pattern, 'morning'),
                self._calculate_time_ratio(pattern, 'afternoon'),
                self._calculate_time_ratio(pattern, 'evening'),
                self._calculate_time_ratio(pattern, 'night'),
                self._calculate_resource_diversity(pattern.get('resources_used', []))
            ]
            features.append(feature_vector)

        return np.array(features)

    def _calculate_subject_diversity(self, subjects: List[Dict]) -> float:
        """Calculate diversity score based on number of different subjects."""
        return len(subjects)

    def _calculate_collaboration_ratio(self, pattern: Dict) -> float:
        """Calculate ratio of collaborative to solo study time."""
        total = pattern.get('total_study_duration', 1)
        collab = pattern.get('collaborative_study_time', 0)
        return collab / total if total > 0 else 0

    def _calculate_time_ratio(self, pattern: Dict, time_of_day: str) -> float:
        """Calculate ratio of study time in specific time period."""
        total = pattern.get('total_study_duration', 1)
        time_dist = pattern.get('time_of_day_distribution', {})
        time_minutes = time_dist.get(time_of_day, 0)
        return time_minutes / total if total > 0 else 0

    def _calculate_resource_diversity(self, resources: List[Dict]) -> float:
        """Calculate diversity of resource types used."""
        if not resources:
            return 0
        unique_types = len(set([r.get('type') for r in resources]))
        return unique_types

    def determine_optimal_k(self, X: np.ndarray, k_range: range = range(2, 11)) -> int:
        """
        Determine optimal number of clusters using elbow method.

        Args:
            X: Feature matrix
            k_range: Range of k values to try

        Returns:
            Optimal k value
        """
        inertias = []

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)

        # Find elbow point (simplified: use maximum second derivative)
        if len(inertias) >= 3:
            second_derivatives = []
            for i in range(1, len(inertias) - 1):
                second_deriv = inertias[i-1] - 2*inertias[i] + inertias[i+1]
                second_derivatives.append(second_deriv)

            # Find maximum second derivative
            elbow_idx = np.argmax(second_derivatives) + 1
            optimal_k = list(k_range)[elbow_idx]
        else:
            optimal_k = 3  # Default

        return optimal_k

    def fit(self, learning_patterns: List[Dict]) -> 'LearningPatternClusterer':
        """
        Fit K-Means model to learning pattern data.

        Args:
            learning_patterns: List of learning pattern records

        Returns:
            Self for method chaining
        """
        # Extract features
        X = self.extract_features(learning_patterns)

        # Normalize features
        X_scaled = self.scaler.fit_transform(X)

        # Determine optimal k if not specified
        if self.n_clusters is None:
            self.n_clusters = self.determine_optimal_k(X_scaled)
            print(f"Optimal number of clusters: {self.n_clusters}")

        # Fit K-Means
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )
        self.model.fit(X_scaled)

        # Profile each cluster
        self._profile_clusters(X, self.model.labels_)

        return self

    def predict(self, learning_patterns: List[Dict]) -> np.ndarray:
        """
        Predict cluster labels for new learning pattern data.

        Args:
            learning_patterns: List of learning pattern records

        Returns:
            Array of cluster labels
        """
        if self.model is None:
            raise ValueError("Model must be fitted before prediction")

        X = self.extract_features(learning_patterns)
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def _profile_clusters(self, X: np.ndarray, labels: np.ndarray):
        """
        Create descriptive profiles for each cluster.

        Args:
            X: Original feature matrix
            labels: Cluster labels
        """
        for cluster_id in range(self.n_clusters):
            mask = labels == cluster_id
            cluster_data = X[mask]

            # Calculate mean values for each feature
            mean_values = np.mean(cluster_data, axis=0)

            profile = {
                'cluster_id': cluster_id,
                'size': np.sum(mask),
                'features': {}
            }

            for i, feature_name in enumerate(self.feature_names):
                profile['features'][feature_name] = mean_values[i]

            # Assign descriptive label
            profile['label'] = self._assign_cluster_label(profile['features'])
            profile['description'] = self._generate_cluster_description(profile['features'])

            self.cluster_profiles[cluster_id] = profile

    def _assign_cluster_label(self, features: Dict[str, float]) -> str:
        """
        Assign a descriptive label to cluster based on dominant characteristics.

        Args:
            features: Dictionary of feature means

        Returns:
            Descriptive label string
        """
        # Determine primary characteristic
        if features['morning_ratio'] > 0.5:
            time_label = "Morning Learner"
        elif features['afternoon_ratio'] > 0.5:
            time_label = "Afternoon Learner"
        elif features['evening_ratio'] > 0.5:
            time_label = "Evening Learner"
        else:
            time_label = "Night Owl"

        # Determine collaboration style
        if features['collaboration_ratio'] > 0.6:
            collab_label = "Highly Collaborative"
        elif features['collaboration_ratio'] > 0.3:
            collab_label = "Balanced"
        else:
            collab_label = "Independent"

        # Determine intensity
        if features['avg_study_duration'] > 5:
            intensity_label = "Intensive"
        elif features['avg_study_duration'] > 3:
            intensity_label = "Moderate"
        else:
            intensity_label = "Light"

        return f"{intensity_label} {time_label} ({collab_label})"

    def _generate_cluster_description(self, features: Dict[str, float]) -> str:
        """
        Generate detailed description of cluster characteristics.

        Args:
            features: Dictionary of feature means

        Returns:
            Description string
        """
        descriptions = []

        # Study duration
        hours = features['avg_study_duration']
        descriptions.append(f"Studies {hours:.1f} hours daily on average")

        # Peak time
        peak = int(features['peak_hour'])
        time_period = "morning" if peak < 12 else "afternoon" if peak < 17 else "evening"
        descriptions.append(f"Most productive in the {time_period}")

        # Collaboration
        collab = features['collaboration_ratio']
        if collab > 0.6:
            descriptions.append("Prefers group study")
        elif collab < 0.3:
            descriptions.append("Prefers solo study")
        else:
            descriptions.append("Balances solo and group study")

        # Subject diversity
        diversity = features['subject_diversity']
        if diversity > 4:
            descriptions.append("Studies wide range of subjects")
        else:
            descriptions.append("Focuses on specific subjects")

        return ". ".join(descriptions) + "."

    def get_cluster_profile(self, cluster_id: int) -> Dict:
        """
        Get detailed profile for a specific cluster.

        Args:
            cluster_id: Cluster ID

        Returns:
            Cluster profile dictionary
        """
        return self.cluster_profiles.get(cluster_id, {})

    def get_all_profiles(self) -> Dict[int, Dict]:
        """
        Get profiles for all clusters.

        Returns:
            Dictionary mapping cluster IDs to profiles
        """
        return self.cluster_profiles

    def visualize_clusters(self, X: np.ndarray, labels: np.ndarray, save_path: str = None):
        """
        Visualize clusters using PCA for dimensionality reduction.

        Args:
            X: Feature matrix
            labels: Cluster labels
            save_path: Optional path to save plot
        """
        # Reduce to 2D using PCA
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X)

        # Plot
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='viridis', alpha=0.6)
        plt.colorbar(scatter)
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
        plt.title('Student Learning Pattern Clusters')

        # Add cluster centers
        centers_2d = pca.transform(self.model.cluster_centers_)
        plt.scatter(centers_2d[:, 0], centers_2d[:, 1],
                   c='red', marker='X', s=200, edgecolors='black', linewidths=2)

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()


# Example usage
if __name__ == "__main__":
    # Sample learning pattern data
    sample_patterns = [
        {
            'total_study_duration': 180,
            'peak_productivity_hour': 14,
            'session_count': 3,
            'subjects_studied': [
                {'subject': 'Math', 'duration': 90},
                {'subject': 'Physics', 'duration': 90}
            ],
            'collaborative_study_time': 60,
            'productivity_score': 7.5,
            'consistency_score': 8.0,
            'time_of_day_distribution': {
                'morning': 60,
                'afternoon': 120,
                'evening': 0,
                'night': 0
            },
            'resources_used': [
                {'type': 'textbook'},
                {'type': 'video'},
                {'type': 'interactive'}
            ]
        },
        # Add more sample patterns...
    ]

    # Create and fit clusterer
    clusterer = LearningPatternClusterer()
    clusterer.fit(sample_patterns)

    # Print cluster profiles
    print("\nCluster Profiles:")
    for cluster_id, profile in clusterer.get_all_profiles().items():
        print(f"\nCluster {cluster_id}: {profile['label']}")
        print(f"Size: {profile['size']} students")
        print(f"Description: {profile['description']}")

## Movie Recommendation System

Project Overview:
This project is a Content-Based Movie Recommendation System that uses various features of movies such as genre, cast, overview, and original title to recommend similar movies based on the user's input. The recommendations are generated using text similarity techniques such as Cosine Similarity and TF-IDF (Term Frequency-Inverse Document Frequency).

Key Features:
1) Content-Based Filtering: The system uses features like genre, overview, and cast to compute similarity between movies.
2) Movie Filtering: Animated, family, and children’s movies can be excluded from recommendations based on user preferences.
3) Movie Recommendations: Provides a list of recommended movies based on an input movie title.

Technologies Used:
- Python: The main programming language used for the implementation.
- Pandas: For data manipulation and handling movie datasets.
- Scikit-learn: For creating the TF-IDF model and computing cosine similarity.
- Regular Expressions: To clean and preprocess text data.
- NumPy: Used for array manipulation and numerical operations.

How It Works:
1) Data Preprocessing:
The dataset is cleaned, with text features (genre, overview, and cast) processed into lowercase and unnecessary characters removed.
The cast is cleaned to remove extra spaces and standardized.
A combined_features column is created, which merges the genre, overview, and cast with different weightings.

2) TF-IDF Vectorization:
The combined_features text data is transformed into a TF-IDF matrix, capturing the importance of each word in the context of the dataset.

3) Cosine Similarity:
Cosine similarity is used to compute the similarity between movies based on the TF-IDF matrix.

4) Movie Recommendation:
The recommendation function receives a movie title, processes it, and compares its similarity against other movies to generate the most similar movie titles. Optional filtering is applied to exclude animated or family movies.

Limitations:
- Limited Data: The recommendation system relies on the quality and quantity of the available dataset. If the dataset doesn't have enough details, the recommendations might not be accurate.

- Content-Based: This implementation focuses purely on content-based filtering and doesn't consider user preferences, which can limit its personalization.

- Complexity of Features: The weightings used for different features might need more fine-tuning to improve the accuracy of recommendations.
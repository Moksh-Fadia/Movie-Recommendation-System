import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("imdb_movies.csv")

movies = movies.dropna(subset=['names', 'genre', 'overview'])

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text)    # remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # remove special characters
    return text.strip()

def clean_crew(crew_str):
    try:
        crew_list = [name.strip() for name in crew_str.split(',')]  
        cleaned = ' '.join([str(name).lower() for name in crew_list])
        return cleaned  
    except:
        return ''  

movies['genre'] = movies['genre'].apply(clean_text)
movies['overview'] = movies['overview'].apply(clean_text)
movies['cast'] = movies['crew'].apply(clean_crew)
movies['names'] = movies['names'].apply(clean_text)

movies['combined_features'] = (
    (movies['overview'] + ' ') * 1 +   
    (movies['genre'] + ' ') * 3 +     # increased weight (for more importance)
    (movies['cast'] + ' ') * 2 +    
    movies['names']
)


tfidf = TfidfVectorizer(stop_words='english')
genre_matrix = tfidf.fit_transform(movies['combined_features'])  # matrix with 0s and 1s for genres
cosine_sim = cosine_similarity(genre_matrix)    # its a similarity matrix (similarity between movies; values between 0-1)

movies = movies.reset_index()
title_to_index = pd.Series(movies.index, index=movies['names'])  # creates a dictionary-like structure with movie names as keys and their indices as values

def recommend_by_genre(title, num_recommendations=5):
    title = clean_text(title)
    index = title_to_index.get(title)    # gets the index of the movie title (returns None if not found)

    if index is None:
        return "Movie not found in the dataset."
    
    similarity_scores = list(enumerate(cosine_sim[index]))  # gets the similarity scores of all movies with respect to the given movie title
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)  # sorts movies based on their scores in descending order

    recommendations = []
    for i, _ in sorted_scores[1:]:
        genre = movies.loc[i, 'genre']   # gets the genre of the movie
        
        if any(exclusion in genre.lower() for exclusion in ['animation', 'family', 'children']):
            continue

        recommendations.append(movies.loc[i, 'names'])
    
        if len(recommendations) >= num_recommendations:
            break

    return recommendations  # returns the movie titles of the top N movies

print(recommend_by_genre("interstellar", 5))

# ML logic

import pandas as pd
import re
import os
import numpy as np   # bcoz embeddings are stored in numpy arrays
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer   # sentence-transformer (a huggingface library) imports a model to get the semantic embeddings of text data

class MovieRecommender:
    def __init__(self, csv_path):
        self.movies = pd.read_csv(csv_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')   # loads the pre-trained model to get text embeddings; 
        # SentenceTransformer('...') initializes the model and makes it ready for encoding 
        self._prepare_data()
        self._compute_similarity()

    def _clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'\s+', ' ', text)    # remove extra spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # remove special characters
        return text.strip()    
    
    def _clean_crew(self, crew_str):
        try:
            crew_list = [name.strip() for name in crew_str.split(',')]  
            cleaned = ' '.join([str(name).lower() for name in crew_list])
            return cleaned  
        except:
            return ''  
        
    def _prepare_data(self):
        self.movies = self.movies.drop_duplicates(subset=['names'])
        self.movies = self.movies.dropna(subset=['names', 'genre', 'overview'])    

        self.movies['genre'] = self.movies['genre'].apply(self._clean_text)
        self.movies['overview'] = self.movies['overview'].apply(self._clean_text)
        self.movies['cast'] = self.movies['crew'].apply(self._clean_crew)
        self.movies['names'] = self.movies['names'].apply(self._clean_text)

        self.movies['combined_features'] = (
            (self.movies['overview'] + ' ') * 1 +
            (self.movies['genre'] + ' ') * 3 +      # increased weight (for more importance)
            (self.movies['cast'] + ' ') * 2 +
            self.movies['names']
        )

        self.movies = self.movies.reset_index(drop=True)
        self.title_to_index = pd.Series(self.movies.index, index=self.movies['names'])        


    def _compute_similarity(self):
        embedding_file = "data/movie_embeddings.npy"    # file path to save/load precomputed embeddings

        if os.path.exists(embedding_file):   # checks if the file already exists
            print("Loading precomputed embeddings...")  
            self.movie_embeddings = np.load(embedding_file)     # loads the precomputed embeddings from the .npy file
        else:
            print("Computing embeddings for the first time...")
            self.movie_embeddings = self.model.encode(self.movies['combined_features'].tolist(), show_progress_bar=True)  
# converts every movie’s combined text (overview + genre + cast + name) into a dense vector embedding; show_progress_bar=True shows a progress bar while encoding
# self.model.encode(list_of_strings): feeds that list into the transformer model and returns a 2D numpy array        
# self.movie_embeddings shape = (no of rows in the dataset, 384 [embedding size of the model]); Each row = a vector (list of 384 float nos) that encodes the "meaning" of that movie’s combined_features text              
            np.save(embedding_file, self.movie_embeddings)   # saves the computed embeddings to the .npy file for future use
            print("Embeddings computed and saved")

# basically all of this to prevent recomputing embeddings every time the server restarts            

        self.cosine_sim = cosine_similarity(self.movie_embeddings)   # precomputes cosine similarity between all pairs of movie embeddings
        print("Embeddings ready")   


    def recommend(self, title, num_recommendations=5):
        title = self._clean_text(title)
        index = self.title_to_index.get(title)    # gets the index of the movie title (returns None if not found)

        if index is None:
            return {"error": "Movie not found."}
        
        similarity_scores = list(enumerate(self.cosine_sim[index]))  # gets the similarity scores of all movies with respect to the given movie title; eg: [(0, 0.1), (1, 0.2), (2, 0.3)...] where first item is index and second item is similarity score

        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)  # sorts movies based on the second item x[1] ie. scores in descending order

        recommendations = []
        for i, _ in sorted_scores[1:]:   # skips the first movie as it is the same movie
            genre = str(self.movies.loc[i, 'genre'])  # gets the genre of the movie at index i       

            if any(exclusion in genre.lower() for exclusion in ['animation', 'family', 'children']):
                continue

            recommendations.append(self.movies.loc[i, 'names'])

            if len(recommendations) >= num_recommendations:
                break
        
        return {"recommendations": recommendations}     
# recommendations is a list of the recommended/similar movie titles       

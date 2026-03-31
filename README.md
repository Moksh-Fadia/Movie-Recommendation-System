# Movie Content Similarity System

A content-based **Movie Recommendation System** built using **Flask** and **Sentence Transformers** that suggests similar movies based on user input.  
It also keeps track of recent searches using **SQLite** and displays them dynamically on the results page.

---

## Features

- Search any movie and get top 5 similar recommendations instantly.  
- Displays recent search history with timestamps.  
- Simple and clean web interface using Flask + HTML/CSS.  

---

## Performance Optimization

- Reduced application startup time by precomputing and caching sentence embeddings using NumPy.
- Improved startup from ~63 seconds to ~0.24 seconds (~99.6% reduction) by avoiding repeated model inference.
- Ensures instant server readiness after initial setup.

---

## Performance Measurement

- Measured end-to-end request latency including database operations, recommendation logic, and template rendering.
- Achieved an average response time of ~15 ms per request during local testing.

---

## Tech Stack

**Backend:** Python, Flask, SQLite  
**ML/NLP:** SentenceTransformers (`all-MiniLM-L6-v2`), Scikit-learn (cosine similarity)  
**Frontend:** HTML, CSS, Jinja2 Templates  
**Libraries:** Pandas, NumPy  

---

## How It Works

User enters a movie name in the search box.
The system encodes the movie’s combined metadata (overview, genre, cast) using the SentenceTransformer model.
It calculates cosine similarity between movies to find the most semantically similar ones.
Results and recent searches are rendered dynamically via Flask and Jinja templates.

---

## Database

The app uses SQLite (app/search_history.db) to store recent searches:

id (auto-increment primary key)
title (searched movie name)
timestamp (search time)

---

# Install dependencies

pip install -r requirements.txt

# Run the Flask App

python main.py

# Access the web app

Go to: http://127.0.0.1:5000/search

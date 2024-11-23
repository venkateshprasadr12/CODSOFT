import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import imdb
from collections import defaultdict

class IMDBMovieRecommender:
    def __init__(self):
        # Initialize the IMDb API
        self.ia = imdb.IMDb()
        
        # Store movie data
        self.movies = {}  # IMDb ID -> movie object
        self.movie_ratings = defaultdict(dict)  # user_id -> {movie_id -> rating}
        self.movie_features = {}  # IMDb ID -> feature vector
        
    def fetch_movie_details(self, movie_id):
        """Fetch movie details from IMDb"""
        if movie_id not in self.movies:
            movie = self.ia.get_movie(movie_id)
            self.movies[movie_id] = {
                'title': movie.get('title', ''),
                'year': movie.get('year', ''),
                'genres': movie.get('genres', []),
                'director': [d.get('name', '') for d in movie.get('directors', [])],
                'cast': [a.get('name', '') for a in movie.get('cast', [])[:5]],
                'rating': movie.get('rating', 0.0)
            }
        return self.movies[movie_id]

    def search_movie(self, title):
        """Search for a movie by title"""
        movies = self.ia.search_movie(title)
        if not movies:
            return None
        
        # Return the top 5 matches
        results = []
        for movie in movies[:5]:
            movie_id = movie.getID()
            # Fetch full movie details
            details = self.fetch_movie_details(movie_id)
            results.append({
                'id': movie_id,
                'title': details['title'],
                'year': details['year'],
                'rating': details['rating']
            })
        return results

    def add_user_rating(self, user_id, movie_id, rating):
        """Add a user rating for a movie"""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
            
        # Ensure we have movie details
        self.fetch_movie_details(movie_id)
        self.movie_ratings[user_id][movie_id] = rating
        
    def calculate_movie_similarity(self, movie_id1, movie_id2):
        """Calculate similarity between two movies based on features"""
        movie1 = self.movies[movie_id1]
        movie2 = self.movies[movie_id2]
        
        # Calculate genre similarity
        genres1 = set(movie1['genres'])
        genres2 = set(movie2['genres'])
        genre_sim = len(genres1.intersection(genres2)) / len(genres1.union(genres2)) if genres1 or genres2 else 0
        
        # Calculate director similarity
        directors1 = set(movie1['director'])
        directors2 = set(movie2['director'])
        director_sim = len(directors1.intersection(directors2)) / len(directors1.union(directors2)) if directors1 or directors2 else 0
        
        # Calculate cast similarity
        cast1 = set(movie1['cast'])
        cast2 = set(movie2['cast'])
        cast_sim = len(cast1.intersection(cast2)) / len(cast1.union(cast2)) if cast1 or cast2 else 0
        
        # Weighted similarity
        return 0.5 * genre_sim + 0.3 * director_sim + 0.2 * cast_sim

    def get_recommendations(self, user_id, n_recommendations=5):
        """Get movie recommendations for a user"""
        if user_id not in self.movie_ratings:
            raise ValueError("User not found")
            
        # Get movies rated by the user
        rated_movies = set(self.movie_ratings[user_id].keys())
        
        # Calculate recommendations
        recommendations = []
        for movie_id in self.movies:
            if movie_id not in rated_movies:
                # Calculate weighted rating based on similar movies
                similarity_scores = []
                weighted_ratings = []
                
                for rated_movie_id, rating in self.movie_ratings[user_id].items():
                    similarity = self.calculate_movie_similarity(movie_id, rated_movie_id)
                    if similarity > 0:
                        similarity_scores.append(similarity)
                        weighted_ratings.append(rating * similarity)
                
                if similarity_scores:
                    predicted_rating = sum(weighted_ratings) / sum(similarity_scores)
                    recommendations.append((
                        movie_id,
                        predicted_rating,
                        self.movies[movie_id]['title'],
                        self.movies[movie_id]['year']
                    ))
        
        # Sort by predicted rating and return top n
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]

def main():
    # Initialize recommender
    recommender = IMDBMovieRecommender()
    
    while True:
        print("\n1. Search for a movie")
        print("2. Rate a movie")
        print("3. Get recommendations")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            title = input("Enter movie title to search: ")
            results = recommender.search_movie(title)
            if results:
                print("\nSearch results:")
                for i, movie in enumerate(results, 1):
                    print(f"{i}. {movie['title']} ({movie['year']}) - IMDb Rating: {movie['rating']}")
            else:
                print("No movies found.")
                
        elif choice == '2':
            user_id = input("Enter your user ID: ")
            title = input("Enter movie title to rate: ")
            results = recommender.search_movie(title)
            
            if results:
                print("\nSearch results:")
                for i, movie in enumerate(results, 1):
                    print(f"{i}. {movie['title']} ({movie['year']})")
                    
                movie_choice = int(input("Select movie number: ")) - 1
                if 0 <= movie_choice < len(results):
                    rating = float(input("Enter rating (1-5): "))
                    recommender.add_user_rating(user_id, results[movie_choice]['id'], rating)
                    print("Rating added successfully!")
                else:
                    print("Invalid selection.")
            else:
                print("No movies found.")
                
        elif choice == '3':
            user_id = input("Enter your user ID: ")
            try:
                recommendations = recommender.get_recommendations(user_id)
                print("\nRecommended movies:")
                for movie_id, rating, title, year in recommendations:
                    print(f"{title} ({year}) - Predicted rating: {rating:.2f}/5")
            except ValueError as e:
                print(e)
                
        elif choice == '4':
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
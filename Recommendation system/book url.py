import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
from collections import defaultdict

class BookRecommender:
    def __init__(self):
        # Store book data
        self.books = {}  # Book ID -> book object
        self.user_ratings = defaultdict(dict)  # user_id -> {book_id -> rating}
        
    def fetch_book_details(self, book_id):
        """Fetch book details using a book API"""
        if book_id not in self.books:
            # Example API call (replace with a real book API endpoint and API key)
            url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
            response = requests.get(url)
            book_data = response.json()
            
            self.books[book_id] = {
                'title': book_data.get('volumeInfo', {}).get('title', ''),
                'authors': book_data.get('volumeInfo', {}).get('authors', []),
                'year': book_data.get('volumeInfo', {}).get('publishedDate', '').split('-')[0],
                'genres': book_data.get('volumeInfo', {}).get('categories', []),
                'rating': book_data.get('volumeInfo', {}).get('averageRating', 0.0)
            }
        return self.books[book_id]

    def search_book(self, title):
        """Search for a book by title"""
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": title, "maxResults": 5}
        response = requests.get(url, params=params)
        books = response.json().get('items', [])
        
        results = []
        for book in books:
            book_id = book.get('id')
            details = self.fetch_book_details(book_id)
            results.append({
                'id': book_id,
                'title': details['title'],
                'year': details['year'],
                'rating': details['rating']
            })
        return results

    def add_user_rating(self, user_id, book_id, rating):
        """Add a user rating for a book"""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
            
        self.fetch_book_details(book_id)
        self.user_ratings[user_id][book_id] = rating

    def calculate_book_similarity(self, book_id1, book_id2):
        """Calculate similarity between two books based on features"""
        book1 = self.books[book_id1]
        book2 = self.books[book_id2]
        
        # Calculate genre similarity
        genres1 = set(book1['genres'])
        genres2 = set(book2['genres'])
        genre_sim = len(genres1.intersection(genres2)) / len(genres1.union(genres2)) if genres1 or genres2 else 0
        
        # Calculate author similarity
        authors1 = set(book1['authors'])
        authors2 = set(book2['authors'])
        author_sim = len(authors1.intersection(authors2)) / len(authors1.union(authors2)) if authors1 or authors2 else 0
        
        # Weighted similarity
        return 0.7 * genre_sim + 0.3 * author_sim

    def get_recommendations(self, user_id, n_recommendations=5):
        """Get book recommendations for a user"""
        if user_id not in self.user_ratings:
            raise ValueError("User not found")
        
        rated_books = set(self.user_ratings[user_id].keys())
        recommendations = []
        
        for book_id in self.books:
            if book_id not in rated_books:
                similarity_scores = []
                weighted_ratings = []
                
                for rated_book_id, rating in self.user_ratings[user_id].items():
                    similarity = self.calculate_book_similarity(book_id, rated_book_id)
                    if similarity > 0:
                        similarity_scores.append(similarity)
                        weighted_ratings.append(rating * similarity)
                
                if similarity_scores:
                    predicted_rating = sum(weighted_ratings) / sum(similarity_scores)
                    recommendations.append((
                        book_id,
                        predicted_rating,
                        self.books[book_id]['title'],
                        self.books[book_id]['year']
                    ))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]

def main():
    recommender = BookRecommender()
    
    while True:
        print("\n1. Search for a book")
        print("2. Rate a book")
        print("3. Get recommendations")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            title = input("Enter book title to search: ")
            results = recommender.search_book(title)
            if results:
                print("\nSearch results:")
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book['title']} ({book['year']}) - Rating: {book['rating']}")
            else:
                print("No books found.")
                
        elif choice == '2':
            user_id = input("Enter your user ID: ")
            title = input("Enter book title to rate: ")
            results = recommender.search_book(title)
            
            if results:
                print("\nSearch results:")
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book['title']} ({book['year']})")
                    
                book_choice = int(input("Select book number: ")) - 1
                if 0 <= book_choice < len(results):
                    rating = float(input("Enter rating (1-5): "))
                    recommender.add_user_rating(user_id, results[book_choice]['id'], rating)
                    print("Rating added successfully!")
                else:
                    print("Invalid selection.")
            else:
                print("No books found.")
                
        elif choice == '3':
            user_id = input("Enter your user ID: ")
            try:
                recommendations = recommender.get_recommendations(user_id)
                print("\nRecommended books:")
                for book_id, rating, title, year in recommendations:
                    print(f"{title} ({year}) - Predicted rating: {rating:.2f}/5")
            except ValueError as e:
                print(e)
                
        elif choice == '4':
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
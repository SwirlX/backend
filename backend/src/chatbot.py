import openai
import wishlist


DB_PATH = "../db/mydb.db"

def generate_query(user_id, con, cur, user_query):
    """
    Generates a response to the user's chatbot query

    Parameters:
        user_id: The id of the user
        con: The connection to the database
        cur: The db cursor
        user_query: The user's query

    Returns:
        Dict: {message}

    """
    rows = wishlist.extract_wish_list_from_db(user_id, con, cur)
    wishlist_movies = wishlist.show_wish_list_movie_data(rows, con, cur)
    returned_data_list = wishlist_movies["wishlist"]

    movie_name_list = []

    for movie in returned_data_list:
        movie_name_list.append(movie['primaryTitle'])
            
    movie_list_string = ','.join(movie_name_list)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"I like {movie_list_string}, {user_query}"}]
    )  
    recommendation_list = completion["choices"][0]["message"]["content"]
    return {"message": recommendation_list}
    



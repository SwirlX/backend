import requests
import json

# Send a GET request to the API endpoint
API_KEY = "1b40f27811f55a1f1cc9ea1f3c148614"

# Example:
# https://api.themoviedb.org/3/find/550?api_key=1b40f27811f55a1f1cc9ea1f3c148614

def get_movie_poster(tconst):
    """
    Will get the post image of a movie given its tconst

    Parameters:
        tconst: The tconst movie id of the movie

    Returns:
        string
    """
    response = requests.get(f'https://api.themoviedb.org/3/find/{tconst}?api_key={API_KEY}&external_source=imdb_id')
    if response.status_code != 200:
        print(f'Request failed with status code {response.status_code}: {response.text}')
        return ""
    
    res = response.json()
    if res["movie_results"] is None or res["movie_results"] == []:
        return "https://scottyscinemas.com.au/Content/Images/Movies//default-movie.png"
    
    if res["movie_results"][0]["poster_path"] is None:
        return "https://scottyscinemas.com.au/Content/Images/Movies//default-movie.png"
        
    full_img_url = 'https://image.tmdb.org/t/p/w500' + res['movie_results'][0]['poster_path']
    return full_img_url
        
if __name__ == "__main__":
    print(f"url -> {get_movie_poster('tt0ad2')}  |")
    

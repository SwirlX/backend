import requests
import error
import sys

API_KEY = "1b40f27811f55a1f1cc9ea1f3c148614"
BASE_API_URL = "https://api.themoviedb.org/3"

def get_tmdb_movie_id(tconst):
    """
   Convert a tconst to a tmdb movie id for use with tmdb

    Parameters:
        tconst

    Returns:
        string: tconst
    """
    response = requests.get(f'{BASE_API_URL}/find/{tconst}?api_key={API_KEY}&external_source=imdb_id')
    if response.status_code != 200:
        raise error.BadRequest("Could not find movie in tmdb")
    
    res = response.json()
    if res["movie_results"] is None or res["movie_results"] == []:
        raise error.AccessError("Malformed movie response. Movie might not exist in tmdb")

    return res["movie_results"][0]["id"]

def get_all_movie_details(tconst):
    """
    Retrieve all details about a movie 

    Parameters:
        tconst

    Returns:
        Dict
    """
    tmdb_movie_id = get_tmdb_movie_id(tconst)
    response = requests.get(f'{BASE_API_URL}/movie/{tmdb_movie_id}?api_key={API_KEY}')
    if response.status_code != 200:
        raise error.BadRequest("Could not find movie in tmdb")
    
    res = response.json()

    return res

def get_similar_movies(tconst):
    """
    Retrieve all details about a movie 

    Parameters:
        tconst

    Returns:
        Dict
    """

    tmdb_movie_id = get_tmdb_movie_id(tconst)
    response = requests.get(f'{BASE_API_URL}/movie/{tmdb_movie_id}/similar?api_key={API_KEY}')
    if response.status_code != 200:
        raise error.BadRequest("Could not find movie in tmdb")
    
    res = response.json()

    img_url_base = 'https://image.tmdb.org/t/p/w500'
    for result in res.get("results"):
        og_path = result["poster_path"]
        if og_path is None:
            result["poster_path"] = "https://scottyscinemas.com.au/Content/Images/Movies//default-movie.png"
        else:
            result["poster_path"] = img_url_base + og_path

        try:
            movie_tconst = get_imdb_tconst_from_tmdb_id(result["id"])
        except:
            movie_tconst = None

        result["tconst"] = movie_tconst

    return res
    

def get_imdb_tconst_from_tmdb_id(tmdb_movie_id):
    """
    Convert a tmdb movie id to imdb tconst

    Parameters:
        tmdb_movie_id: The tmdb movie id to convert

    Returns:
        tconst: string
    """
    response = requests.get(f'{BASE_API_URL}/movie/{tmdb_movie_id}?api_key={API_KEY}')
    if response.status_code != 200:
        raise error.BadRequest("Could not find movie in tmdb")
    
    res = response.json()
    return res["imdb_id"] 

def check_movie_is_age_safe(tconst):
    tmdb_movie_id = get_tmdb_movie_id(tconst)
    response = requests.get(f'{BASE_API_URL}/movie/{tmdb_movie_id}/release_dates?api_key={API_KEY}')
    if response.status_code != 200:
        raise error.BadRequest("Could not find movie in tmdb")
    
    res = response.json()
    results = res['results'] 
    # print(results)
    for result in results:
        if result['iso_3166_1'] == "US":
            # print(result['release_dates'])
            release_date = result['release_dates']
            certification = release_date[0]['certification']

            return certification == 'G' or certification == 'PG'
    # return True



if __name__ == "__main__":
    tconst = sys.argv[1]
    print(get_tmdb_movie_id(tconst))

    
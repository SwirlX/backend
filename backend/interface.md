# Interface

|Name|HTTP Method|Parameters|Return|Exceptions|Description|
|----|-----------|----------|------|----------|-----------|
|/auth/register|POST|  (email, password, first_name, last_name, dob)  | {user_id, token} | **InputError** when any of:<ul><li>Email entered is not a valid email using regex</li><li>Email address is already being used by another user</li></ul> | Register a user |
|/auth/login|POST|  (email, password)  | {user_id, token} | N/A | Login user |
|/auth/logout|POST|  (token)  | {is_success} | N/A | Logout user |
|/auth/password-reset/request|POST| (email) | {} | N/A | Given an email address, if the user is a registered user, send's them a an email containing a specific secret code, that when entered in auth_passwordreset_reset, shows that the user trying to reset the password is the one who got sent this email |
|/auth/password-reset/reset|POST|  (reset_code, new_password)  | {} | N/A | Given a reset code for a user, set that user's new password to the password provided |
|/user/edit|POST|  (username, first_name, last_name, password, email, dob)  | {is_success} | Possible Exceptions? | Logout user |
|/search/\<keyword\>| GET | path_param: keyword | {tconst, primaryTitle, year, genres, rating, poster_image} | N/A | Search for a movie given a keyword|
|reviews/create|POST| (user_id, tconst, rating, review_text) | {} | **DatabaseError** & **InputError** if tconst, user doesn't exist | Create a review for a movie
|/reviews/get-review-id|GET|(user_id, tconst, rating, review_text) | {review_id} | **InputError** if the review doesn't exist | Gets the review id of a review for a movie
|/reviews/get-review/|GET|(review_id)|{user_id, tconst, rating, review_text}|**InputError** if review doesn't exist| Gets all review details given a review id
|/reviews/get-movie-reviews| GET | (tconst) | {reviews} | N/A | Get all the reviews for a given movie
|/reviews/get-user-reviews| GET | (user_id) | {reviews} | **InputError** if user doesn't exist | Get all the reviews made by a user|
|/reviews/update-review-text| PUT | (review_id, new_review_text) | {} | **DatabaseError** & **InputError** if the review doesn't doesn't exist | Update the review text of an existing review from a user
|/reviews/delete|DELETE|(review_id)|{}|**InputError** if review doesn't exist| Delete a review
|/movie/get-movie-details/<tconst>|GET|path_param: tconst|{title, year, genres}|**DatabseError** if movie doesn't exist | Retrieve movie details given a tconst|
|/user/get-user-details/<user_id>|GET|path_param: user_id| {first_name, last_name, email, dob, token} | **InputError** if user not found |Retrieve user details given a user id|
 
  
 # Sprint 2
  |Name|HTTP Method|Parameters|Return|Exceptions|Description|
|----|-----------|----------|------|----------|-----------|
|/search/actor/<actor_name>|GET|(actor_name)|{tconst, primaryTitle, year, genres, rating, poster_image}| **InputError** if not found, or input is of invalid form| Get the movies with certain actors |
|/search/genre/<genre_name>|GET|(genre_name)|{tconst, primaryTitle, year, genres, rating, poster_image}| **InputError** if not found, or input is of invalid form| Get the movies of certain genres |
|/search/year/<year>|GET|(year)|{tconst, primaryTitle, year, genres, rating, poster_image}| **InputError** if not found, or input is of invalid form| Get the movies starting in a certain year|
|/search/title/<title>|GET|(title)|{tconst, primaryTitle, year, genres, rating, poster_image}| **InputError** if not found, or input is of invalid form| Get the movies of a certain title substring|
|/recommendations/<tconst>|GET|(genre, actor?)|{tconst, primaryTitle, year, genres, rating, poster_image} | N/A | Get a list of recommendations for movies based off the current movie being viewed.|
|/discussion/create|POST|(discussion_title, discussion_description, datetime)|{discussion_id}|N/A| Create a discussion post |
|/discussion/delete/<discussion_id>|DELETE|(discussion_id)|{}|**Error** Discussion post doesn't exist| Delete a discussion post|
|/discussion/get-all-discussion-posts|GET|()|{discussionPosts}|N/A| Get all discussion posts |
|/discussion/comment/create|POST|(discussion_id, comment_text, datetime)|{comment_id}|**Error** discussion post doesn't exist | Comment on a created discussion post |
|/discussion/comment/delete/<comment_id>|DELETE|(comment_id)|{}|**Error** comment doesn't exist| Delete a comment on a discussion post|
|/discussion/get-discussion-post/<discussion_id>|GET|(discussion_id)|{discussion_title, discussion_description, discussion_comments}|**Error** Discussion post doesn't exist| Get all details of the discussion including title, description and comments |
|/movie/get-movie-actors/<tconst>|GET|<tconst>|{actors}|N/A| Get list of actors in a particular movie|
|/movie/get-movie-directors/<tconst>|GET|<tconst>|{directors}|N/A| Get list of directors in a particular movie|
|/chatbot/??|
|/wishlist/add|PUT|{userid, tconst}|{wishlist}|N/A| Add to wishlist of user|
|/wishlist/view|GET|<tconst>|{wishlist}|N/A| Get wihslist of user|
 
 



 

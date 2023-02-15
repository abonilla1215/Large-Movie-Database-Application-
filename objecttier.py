#
# File: objecttier.py
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, id, name, year):
    self._Movie_ID = id
    self._Title = name
    self._Release_Year = year
  @property
  def Movie_ID(self): return self._Movie_ID
  @property
  def Title(self): return self._Title
  @property
  def Release_Year(self): return self._Release_Year

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, id, name, year, views, rank):
    self._Movie_ID = id
    self._Title = name
    self._Release_Year = year
    self._Num_Reviews = views
    self._Avg_Rating = rank
  @property
  def Movie_ID(self): return self._Movie_ID
  @property
  def Title(self): return self._Title
  @property
  def Release_Year(self): return self._Release_Year
  @property
  def Num_Reviews(self): return self._Num_Reviews
  @property
  def Avg_Rating(self): return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, id, name, year, time, lang, cost, profit, views, rank, tag, genre, credits):
    self._Movie_ID = id
    self._Title = name
    self._Release_Date = year
    self._Runtime = time
    self._Original_Language = lang
    self._Budget = cost
    self._Revenue = profit    
    self._Num_Reviews = views
    self._Avg_Rating = rank
    self._Tagline = tag
    self._Genres = genre
    self._Production_Companies = credits
  @property
  def Movie_ID(self): return self._Movie_ID
  @property
  def Title(self): return self._Title
  @property
  def Release_Date(self): return self._Release_Date
  @property
  def Runtime(self): return self._Runtime
  @property
  def Original_Language(self): return self._Original_Language
  @property
  def Budget(self): return self._Budget
  @property
  def Revenue(self): return self._Revenue
  @property
  def Num_Reviews(self): return self._Num_Reviews
  @property
  def Avg_Rating(self): return self._Avg_Rating
  @property
  def Tagline(self): return self._Tagline
  @property
  def Genres(self): return self._Genres
  @property
  def Production_Companies(self): return self._Production_Companies

##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  sql = """select count(Movie_ID)
           from Movies;"""
  total = datatier.select_one_row(dbConn, sql, [])
  if total is None: return -1
  return total[0]
##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  sql = """select count(Rating)
           from Ratings;"""
  total = datatier.select_one_row(dbConn, sql, [])
  if total is None: return -1
  return total[0]
   
##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  sql = """select Movie_ID, Title, strftime('%Y', Release_Date)
            from Movies
            where Title like ?
            group by Movie_ID
            order by Title asc;"""
  total = datatier.select_n_rows(dbConn, sql, [pattern])
  hold = []
  if total is None: return [] # Test case 8?
  for x in total:
    movies = Movie(x[0],x[1],x[2])
    hold.append(movies)
  return hold
  
  


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  # Genre AND Production must be orginized
  # sql1 will hold (id, title, release, time, lang, cost, profit, num reviews, rating, ___, ___, tagline)
  sql1 = """select Movies.Movie_ID,Title, date(Release_Date), Runtime,
            Original_Language, Budget, Revenue,
            count(Rating), avg(Rating),Tagline
            from Movies
            left join Ratings on Movies.Movie_ID = Ratings.Movie_ID
            left join Movie_Taglines on Movies.Movie_ID = Movie_Taglines.Movie_ID
            where Movies.Movie_ID = ?;"""
  # sql 2 will hold (___, ___, ___, ___, ___, ___, ___, ___, ___, Genres, ___, ___)
  sql2 = """select distinct Genre_Name
            from Genres
            left join Movie_Genres on Genres.Genre_ID = Movie_Genres.Genre_ID
            left join Movies on Movie_Genres.Genre_ID = Movies.Movie_ID
            where Movie_Genres.Movie_ID = ?
            order by Genre_Name asc;"""
  # sql 3 will hold (___, ___, ___, ___, ___, ___, ___, ___, ___, ___, Companies, ___)
  sql3 = """select Company_Name 
            from Companies
            left join Movie_Production_Companies on Movie_Production_Companies.Company_ID = Companies.Company_ID
            left join Movies on Movies.Movie_ID = Movie_Production_Companies.Movie_ID
            where Movie_Production_Companies.Movie_ID = ?
            order by Company_Name asc;"""
  # We will then combine the 3 sqls spit out the desired datatier
  Main_Chunk = datatier.select_one_row(dbConn, sql1, [movie_id])
  Genre_Total = datatier.select_n_rows(dbConn, sql2, [movie_id])
  Company_Total = datatier.select_n_rows(dbConn, sql3, [movie_id])

  if Main_Chunk[1] is None: return None
  
  if Main_Chunk[8] is None: Average = 0.0
  else: Average = Main_Chunk[8]
  
  if Main_Chunk[9] is None: Tag = ""
  else: Tag = Main_Chunk[9]
  # Test case 8
  if Genre_Total is None: return None
  if Company_Total is None: return None
    
  Genre_arr = []
  Company_arr = []
  
  for x in Genre_Total:
    Genre_arr.append(x[0])
  for y in Company_Total:
    Company_arr.append(y[0])
  
  movie = MovieDetails(Main_Chunk[0],Main_Chunk[1],Main_Chunk[2],Main_Chunk[3],Main_Chunk[4],Main_Chunk[5],Main_Chunk[6],Main_Chunk[7],Average,Tag, Genre_arr, Company_arr)

  return movie
  
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  sql = """select Movies.Movie_ID,Title, strftime('%Y', Release_Date),
           count(Rating), avg(Rating)
           from Movies
           left join Ratings on Movies.Movie_ID = Ratings.Movie_ID
           group by Movies.Movie_ID
           having (count(Rating) >= ?)
           order by avg(Rating) desc
           limit ?;"""
  total = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
  hold = []
  if total is None: return [] # Test case 8?
  for x in total:
    top = MovieRating(x[0], x[1], x[2], x[3], x[4])
    hold.append(top)
  return hold

##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  sql = """Insert Into Ratings
           values(?, ?);"""
  sqlCheck = """Select Title 
                from Movies
                where Movie_ID = ?;"""
  test = datatier.select_one_row(dbConn,sqlCheck, [movie_id])
  if test == (): return 0
  total = datatier.perform_action(dbConn,sql, [movie_id,rating])
  if total == -1: return 0
  return 1
    

##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  sql = """Update Movie_Taglines
           set Tagline = ?
           where Movie_ID = ?;"""
  sqlCheck = """Select Title 
                from Movies
                where Movie_ID = ?;"""
  
  sqlCheck2 = """Select Tagline 
                 from Movie_Taglines 
                 where Movie_ID =?"""
  sql2 = """Insert into Movie_Taglines 
            values(?,?)"""
  
  test = datatier.select_one_row(dbConn,sqlCheck, [movie_id])
  total = datatier.perform_action(dbConn,sql, [tagline,movie_id])
  test2 = datatier.select_one_row(dbConn, sqlCheck2, [movie_id])
  if test == (): return 0
  if total == -1: return 0
  if test2 == (): total2 = datatier.perform_action(dbConn, sql2, [movie_id,tagline]) 
  return 1
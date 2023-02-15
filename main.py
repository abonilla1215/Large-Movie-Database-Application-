# Alex Bonilla
# The goal of this program is the use python and sql together to retrieve and display data from 
# the provided movie data base file. We are charged w/ creating 5 command functions with each 
# function having its own unique action

import sqlite3
import objecttier

#___FUNctions___#

# formats list of movies
def my_own_GetNumMovies(list):
  print("\n# of movies found:", len(list))
  print()

# formats a list
def my_own_PrintList(list):
  for x in list:
    print(x+",", end=" ")
  print()

def print_stats(dbConn):
  statsNum = objecttier.num_movies(dbConn)
  statsRev = objecttier.num_reviews(dbConn)
  print("\nGeneral stats:")
  print("  # of movies:", f"{statsNum:,}")
  print("  # of reviews:", f"{statsRev:,}")
  
#___command functions___#
  
# Takes a movie title as an input and spits out the number
# of results found along with displaying its id, name, and year
def command1(dbConn):
  name = input("\nEnter movie name (wildcards _ and % supported): ")
  Function_1 = objecttier.get_movies(dbConn, name)
  my_own_GetNumMovies(Function_1)
  if len(Function_1) > 100:
    print("\nThere are too many movies to display, please narrow your search and try again...\n")
    return    
  for x in Function_1:
    print(x.Movie_ID, ":", x.Title, f"({x.Release_Year})")

# Takes a movie id as an input and displays ALL details about it
def command2(dbConn):
  id = input("\nEnter movie id: \n")
  Function_2 = objecttier.get_movie_details(dbConn, id)
  if Function_2 is None:
    print("\nNo such movie...")
    return
  print(Function_2.Movie_ID, ":", Function_2.Title)
  print("  Release date:", Function_2.Release_Date)
  print("  Runtime:", Function_2.Runtime, "(mins)") 
  print("  Orig language:", Function_2.Original_Language) 
  print("  Budget:", f"${Function_2.Budget:,}", "(USD)")
  print("  Revenue:", f"${Function_2.Revenue:,}", "(USD)")
  print("  Num reviews:", Function_2.Num_Reviews)
  print("  Avg rating:", f"{Function_2.Avg_Rating:.2f}", "(0..10)")
  print("  Genres:", end = " ") 
  my_own_PrintList(Function_2.Genres)
  print("  Production companies:", end = " ") 
  my_own_PrintList(Function_2.Production_Companies)
  print("  Tagline:", Function_2.Tagline)

# Takes an input of what kind of 'top list' you want (ex: 'top 10')
# and then takes in the MINIMUM number of reviews you want from each list
# after that, the 'top list' is displayed along with the movies id, name, year,
# average rating and number of reviews
def command3(dbConn):
  N = input("\nN? ")
  if int(N) <= 0:
    print("Please enter a positive value for N...")
    return
  Min = input("min number of reviews? ")
  if int(Min) <= 0:
    print("Please enter a positive value for min number of reviews...")
    return
  print()
  Function_3 = objecttier.get_top_N_movies(dbConn, int(N), int(Min)) # won't work unless it's int
  for x in Function_3:
    print(x.Movie_ID, ":", x.Title, f"({x.Release_Year}),", 
          "avg rating =", f"{x.Avg_Rating:.2f}", 
          "(" + str(x.Num_Reviews) + " reviews)")

# Takes a rating number between 0 and 10 and a movie id,
# after that the users input will be put into the movies review database
def command4(dbConn):
  rating = int(input("\nEnter rating (0..10): "))
  if rating < 0 or rating > 10:
    print("Invalid rating...")
    return
  id = input("Enter movie id: ")
  Function_4 = objecttier.add_review(dbConn, id, rating)
  if Function_4 == 0:
    print("\nNo such movie...")
    return
  elif Function_4 == 1:
    print("\nReview successfully inserted")
    return

# Takes a string for a new tagline and a movie id,
# after that the users input will change that specified movie tagline
def command5(dbConn):
  tag = input("\ntagline? ")
  id = input("movie id? ")
  Function_5 = objecttier.set_tagline(dbConn, id, tag)
  if Function_5 == 0:
    print("\nNo such movie...")
    return
  elif Function_5 == 1:
    print("\nTagline successfully set")
    return
##################################################################  
#
# main
#
# Basic set up, you can insert a number between 1 and 5
# if you wish to exit the program type 'x'
print('** Welcome to the MovieLens app **')
dbConn = sqlite3.connect('MovieLens.db')
print_stats(dbConn)
while True:
  User_Input = input("\nPlease enter a command (1-5, x to exit): ")
  if User_Input == 'x': break 
  elif User_Input == '1': command1(dbConn)
  elif User_Input == '2': command2(dbConn)
  elif User_Input == '3': command3(dbConn)
  elif User_Input == '4': command4(dbConn)
  elif User_Input == '5': command5(dbConn)
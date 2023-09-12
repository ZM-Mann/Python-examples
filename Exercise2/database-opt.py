import sqlite3

# Read the file and copy the contents to the list 
with open("./Exercise2/stephen_king_adaptations.txt", "r") as file:
    stephen_king_adaptations_list = [line.strip().split(',') for line in file]

# Establishing a connection to a SQLite database 
connection = sqlite3.connect("./Exercise2/stephen_king_adaptations.db")
cursor = connection.cursor()

# Create tables 
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table 
               (movieID TEXT,movieName TEXT, movieYear INT, imdbRating REAL)''')

# Insert content into a table 
cursor.executemany('INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)', stephen_king_adaptations_list)

# Commit the changes 
connection.commit()

# Function is used to search the database for movies based on the given parameters 
def search_movies(option):
    if option == 1:
        movie_name = input(" Please enter the name of the movie to search for: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
    elif option == 2:
        movie_year = input(" Please enter the the movie to search for: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
    elif option == 3:
        movie_rating = float(input(" Please enter the minimum rating for the movie to search for: "))
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (movie_rating,))
            
    movies = cursor.fetchall()

    if len(movies) > 0:
        for movie in movies:
            print("  Movie name:", movie[1])
            print("  Movie year:", movie[2])
            print("  Movie IMDB rating:", movie[3])
            # print()
    else:
        if option == 1:
            print(" No such movie exists in our database.")
        elif option == 2:
            print(" No movies were found for that year in our database.")
        elif option == 3:
            print(" No movies at or above that rating were found in the database.")

# User interaction loop 
while True:
    print()
    print("The way to search for movies in the database is as follows: ")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")
    choice = int(input("Please enter your choice: "))

    if choice == 4:
        break
    else:
        search_movies(choice)

cursor.execute('DELETE FROM stephen_king_adaptations_table;')
connection.commit()  

# Close the database connection 
connection.close()

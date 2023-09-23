import sqlite3

# Establishing a connection to a SQLite database 
conn = sqlite3.connect('./Exercise4/library.db')
cursor = conn.cursor()

# CREAT Books, Users, Reservations TABLE
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID TEXT NOT NULL,
                    Title TEXT NOT NULL,
                    Author TEXT NOT NULL,
                    ISBN TEXT NOT NULL,
                    Status TEXT NOT NULL
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID TEXT NOT NULL,
                    Name TEXT NOT NULL,
                    Email TEXT NOT NULL
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID TEXT NOT NULL,
                    BookID TEXT,
                    UserID TEXT,
                    ReservationDate TEXT NOT NULL,
                    FOREIGN KEY (BookID) REFERENCES Books (BookID),
                    FOREIGN KEY (UserID) REFERENCES Users (UserID)
                )''')
conn.commit()


# Sample book details:
# LB001, The Alchemist, Paulo Coelho, 978-0062315007, LR-Reserved
# LB002, The Kite Runner, Khaled Hosseini, 978-1594631931, LR-Reserved
# LB003, The Lord of the Rings, J. R. R. Tolkien, 978-0544003415, LR-Available
# cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",("LB001", "The Alchemist", "Paulo Coelho", "978-0062315007", "LR-Reserved"))
# cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",("LB002", "The Kite Runner", "Khaled Hosseini", "978-1594631931", "LR-Reserved"))
# cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",("LB003", "The Lord of the Rings", "J. R. R. Tolkien", "978-0544003415", "LR-Available"))

# user details:
# LU001, John Doe, john.doe@example
# LU002, Jane Doe, jane.doe@example
# LU003, John Smith, john.smith@example
# cursor.execute("INSERT INTO Users (UserID, Name, Email) VALUES (?, ?, ?)",("LU001", "John Doe", "john.doe@example"))
# cursor.execute("INSERT INTO Users (UserID, Name, Email) VALUES (?, ?, ?)",("LU002", "Jane Doe", "jane.doe@example"))
# cursor.execute("INSERT INTO Users (UserID, Name, Email) VALUES (?, ?, ?)",("LU003", "John Smith", "john.smith@example"))

# reservation details:
# LR001, LB001, LU001, 2020-01-01
# LR002, LB002, LU002, 2020-01-02
# LR003, LB003, LU003, 2020-01-03
# cursor.execute("INSERT INTO Reservations (ReservationID, BookID, UserID, ReservationDate) VALUES (?, ?, ?, ?)",("LR001", "LB001", "LU001", "2020-01-01"))
# cursor.execute("INSERT INTO Reservations (ReservationID, BookID, UserID, ReservationDate) VALUES (?, ?, ?, ?)",("LR002", "LB002", "LU002", "2020-01-02"))
# conn.commit()


# Function to add a new book to the database
def add_book():
    bookID = input("Enter the bookID(starts with LB): ")
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    isbn = input("Enter the book ISBN: ")
    status = input("Enter the book status: ")
    
    cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)", (bookID, title, author, isbn, status))

    conn.commit()
    print("Book added successfully!")


# Function to find a book's details based on BookID
def find_book_details():
    book_id = input("Enter the BookID(starts with LB): ")
    
    cursor.execute('''SELECT Books.*, Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                      WHERE Books.BookID = ?''', (book_id,))
    
    book_details = cursor.fetchone()
    
    if book_details:
        print("BookID:", book_details[0])
        print("Title:", book_details[1])
        print("Author:", book_details[2])
        print("ISBN:", book_details[3])
        print("Status:", book_details[4])
        
        if book_details[5]:
            print("Reserved by:", book_details[5])
            print("User Email:", book_details[6])
        else:
            print("Not reserved")
    else:
        print("Book not found")


# Function to find a book's reservation status based on BookID, Title, UserID, or ReservationID
def find_reservation_status():
    search_text = input("Enter the BookID, Title, UserID, or ReservationID: ")
    
    if search_text.startswith("LB"):
        cursor.execute('''SELECT Books.Status, Books.Title, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.BookID = ?''', (search_text,))
    elif search_text.startswith("LU"):
        cursor.execute('''SELECT Books.Status, Books.Title, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Users.UserID = ?''', (search_text,))
    elif search_text.startswith("LR"):
        cursor.execute('''SELECT Books.Status, Books.Title, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Reservations.ReservationID = ?''', (search_text,))
    else:
        cursor.execute('''SELECT Books.Status, Books.Title, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.Title = ?''', (search_text,))
    
    reservation_status = cursor.fetchone()
    
    if reservation_status:
        print("Reservation Status:", reservation_status[0])
        print("Book Title:", reservation_status[1])
        
        if reservation_status[2]:
            print("Reserved by:", reservation_status[2])
            print("User Email:", reservation_status[3])
        else:
            print("Not reserved")
    else:
        print("Book not found")


# Function to find all the books in the database
def find_all_books():
    cursor.execute('''SELECT Books.*, Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    
    all_books = cursor.fetchall()
    
    if all_books:
        for book in all_books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            
            if book[5]:
                print("Reserved by:", book[5])
                print("User Email:", book[6])
            else:
                print("Not reserved")
            
            print()
    else:
        print("No books found")


# Function to modify/update book details based on BookID
def modify_book_details():
    book_id = input("Enter the BookID: ")
    
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        print("Current Book Details:")
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        
        choice = input("Do you want to update the reservation status? (Y/N): ")
        
        if choice.lower() == "y":
            new_status = input("Enter the new reservation status: ")
            ReservationID = input("Enter the ReservationID: ")
            ReservationDate = input("Enter the ReservationDate: ")
            UserID = input("Enter the UserID: ")
            Name = input("Enter the Name: ")
            Email = input("Enter the Email: ")

            cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))

            cursor.execute("INSERT INTO Users (UserID, Name, Email) VALUES (?, ?, ?)", (UserID, Name, Email))
            
            cursor.execute("INSERT INTO Reservations (ReservationID, BookID, UserID, ReservationDate) VALUES (?, ?, ?, ?)",(ReservationID, book_id, UserID, ReservationDate))
            conn.commit()
            print("Book details updated successfully!")
        else:
            print("No changes made")
    else:
        print("Book not found")


# Function to delete a book based on its BookID
def delete_book():
    book_id = input("Enter the BookID: ")
    
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found")


# Main program loop
while True:
    print()
    print("Library Management System")
    print("1. Add a new book to the database")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status based on BookID, Title, UserID, and ReservationID")
    print("4. Find all the books in the database")
    print("5. Modify/update book details based on its BookID")
    print("6. Delete a book based on its BookID")
    print("7. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_details()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        modify_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break


# Close the database connection 
conn.close()
# Collaborators: Mohamed Abdulmalik (mma6599), Siddharth Anmalsetty (ssa5526), Avyukt Singh (aps6951)

####################################################    FUNCTIONS/METHODS    ############################################################


def sort2DArray(array):
    
    notSorted = True

    
    while notSorted == True:
        i = 0
        notSorted = False
        tempEntry = ["",0]
        while i < len(array) - 1:
            currentEntry = ["", 0]
            currentEntry[0] = array[i][0]
            currentEntry[1] = array[i][1]
            if currentEntry[1] > array[i+1][1]:
                tempEntry[0] = array[i+1][0]
                tempEntry[1] = array[i+1][1]
                array[i+1][0] = currentEntry[0]                
                array[i+1][1] = currentEntry[1]
                array[i][0] = tempEntry[0]                
                array[i][1] = tempEntry[1]
                notSorted = True

            i += 1



def setUsageRatio():
    for i in bookBorrowCounter:
        for j in totalCopiesCounter:
            if i[0] == j[0]:
                newEntry = []
                usage = getUsage(i[0])
                newEntry = []
                newEntry.append(i[0])
                newEntry.append(usage * 100)
                usageRatios.append(newEntry)

def getUsage(book):
    usage = 0.0
    for i in bookBorrowCounter:
        for j in totalCopiesCounter:
            if i[0] == book and j[0] == book:
                usage = i[1] / j[1]
    
    return usage

def setTotalCopiesPerBook():
    for i in booklist:
        newEntry = []
        newEntry.append(i[0])
        newEntry.append(i[1])
        totalCopiesPerBook.append(newEntry)

def setTotalCopiesCounter():
    for i in booklist:
        newEntry = []
        newEntry.append(i[0])
        newEntry.append(0)
        totalCopiesCounter.append(newEntry)

def updateTotalCopiesCounter():
    for i in totalCopiesCounter:
        for j in totalCopiesPerBook:
            if i[0] == j[0]:
                i[1] = i[1] + j[1]


# updates the boorow counter for each book in bookBorrowCounter[]
def updateBookBorrowCounter():
    for i in borrowed:
        for j in bookBorrowCounter:
            if i[3] == j[0]:
                j[1] = j[1] + 1


#Returns an int of the total copies available for a book on the current day
def getTotalNumOfCopies(book):
    totalCopies = 0
    for i in booklist:
        if i[0] == book:
            totalCopies += int(i[1])
    for i in borrowed:
        if i[3] == book:
            totalCopies += 1
    return totalCopies

# Returns True if the person can borrow a book given a Borrow line in libLog and False if they can not
def canBorrow(entry):
    # Format of entry: B#<day>#<Student Name>#<Book name>#<days borrowed for>

    canBorrow = False
    for b in booklist:
        if b[0] == entry[3]:
            canBorrow = True


    # Checks if the person has any fees or more than 3 books checked out
    if getOutstandingFines(entry[2]) > 0:
        canBorrow = False
    if getOutstandingBooks(entry[2]) >= 3:
        canBorrow = False
    
    # Checks if the person already has this book borrowed
    alreadyBorrowed = False
    for b in borrowed:
        if b[2] == entry[2] and b[3] == entry[3]:
            alreadyBorrowed = True
    if alreadyBorrowed == True:
        canBorrow = False
    
    if dayCounter == 166 or lineNum == 389:
        print("", end = "")
    #Checks if there are copies available
    for b in booklist:
        if b[0] == entry[3]:
            if b[1] <= 0:
                canBorrow = False

        """if b[1] >= 1:
                b[1] -= 1
            else:
                print("", end = "") # Used to be: print("There are no more coppies of that book")
                canBorrow = False"""
    
    #Checks if they are borrowing the book for too long
    for b in booklist:
        if b[0] == entry[3]:
            if b[2] == "TRUE" and int(entry[4]) > 7:
                canBorrow = False
            elif b[2] == "FALSE" and int(entry[4]) >28:
                canBorrow = False
    
    #Returns True if the book can be borrowed and False if it can't
    return canBorrow


def Borrow(entry):
    # Format of entry: B#<day>#<Student Name>#<Book name>#<days borrowed for>

    # check if the person can borrow the book
    if canBorrow(entry) == False:
        print("", end = "") # used to be: print("Book can not be borrowed")
    else:

        # convert the current day and the borrow length to numbers
        entry[1] = int(entry[1])
        entry[4] = int(entry[4])
        
        # add this entry to the borrowed array
        borrowed.append(entry)

        # Subtract one form the number of copies available
        for b in booklist:
            if b[0] == entry[3]:
                b[1] -= 1
                



def Return(entry):
    #Format of entry: R#<Day>#<Student Name>#<Book Name>

    #convert the date into a number
    entry[1] = int(entry[1])

    #add this entry to the returned array
    returned.append(entry)

    #adds one to the number of book copies available 
    for b in booklist:
        if b[0] == entry[3]:
            b[1] += 1
    
    #Check if the book was returned late, calculates the fine, and adds it to the oustandingFines[] array
    for b in borrowed:
        if b[2] == entry[2] and b[3] == entry[3]:
            if b[1] + b[4] < currentLineDay:
                # Increments bookBorrowCounter
                for c in bookBorrowCounter:
                    if c[0] == entry[3]:
                        c[1] = c[1] + (entry[1] - (b[1] + b[4]))

                # Determines the fine
                for l in booklist:
                    if entry[3] == l[0]:
                        if l[2] == "TRUE":
                            addedFine = 5 * (entry[1] - (b[1] + b[4]))
                        else:
                            addedFine = entry[1] - (b[1] + b[4])
                nameFound = False
                i = 0
                while i < len(outstandingFines) and nameFound == False:
                    if outstandingFines[i][1] == entry[2]:
                        nameFound = True 
                        outstandingFines[i][2] += addedFine
                    i += 1
                if nameFound == False:
                    # format of newOutstandingFineEntry: Student name - Amount owed
                    newOutstandingFineEntry = [entry[2], addedFine]
                    outstandingFines.append(newOutstandingFineEntry)
    
    # Updates borrowed[] by removing the corresponding entry from it
    counter = 0
    while counter < len(borrowed):
        if borrowed[counter][2] == entry[2] and borrowed[counter][3] == entry[3]:
            borrowed.pop(counter)
        counter += 1


def Addition(entry):
    # Format of entry: A#<day>#<Book name>
    # Format of booklist: <Book Name>#<num of copies>#<regulation>

    # If bookFound remains false, it adds a new book to bookList.
    # If bookFound becomes True, then one copy is added to the book in bookList
    bookFound = False
    i = 0
    while i < len(booklist) and bookFound == False:
        if booklist[i][0] == entry[2]:
            bookFound = True
            booklist[i][1] = booklist[i][1] + 1
            for j in totalCopiesPerBook: # increase the totalCopiesCounter for this book by one
                if j[0] == booklist[i][0]:
                    j[1] = j[1] + 1
        i += 1
    if bookFound == False:
        newBook = []             # Creates an array to hold the information for the book being added
        newBook.append(entry[2]) # Adds the book's name
        newBook.append(1)        # Sets the number of copies to 1
        newBook.append(False)    # Sets the regulation to False
        booklist.append(newBook) # Adds the the new book to booklist


    # Adds this book to bookBorrowCounter
    if bookFound == False:
        newEntry = []
        newEntry.append(entry[2])           # Sets the book name
        newEntry.append(0)                  # Sets the days borrowed to 0
        bookBorrowCounter.append(newEntry)  # Adds this book to bookBorrowCounter[] array
    

    # Adds this book to totalCopiesPerBook[]
    if bookFound == False:
        newEntry = []
        newEntry.append(entry[2])
        newEntry.append(1)
        totalCopiesPerBook.append(newEntry)
    
    # Adds this book to totalCopiescounter[]
    if bookFound == False:
        newEntry = []
        newEntry.append(entry[2])
        newEntry.append(0)
        totalCopiesCounter.append(newEntry)


def Fine(entry):
    #Entry Format: P#<day>#<student name>#<amount>
    
    #convert amount to an int
    entry[3] = int(entry[3])


    #Format of newOutstandingFineEntry: [<Student Name>, <Amount Owed>]
    #This subtracts the amount being paid from the amount that is owed
    for i in outstandingFines:
        if i[0] == entry[2]:
            i[1] = i[1] - entry[3]
    
    
#Returns and int of how many books the person currently has checked out
def getOutstandingBooks (name):
    booksBorrowed = 0
    booksReturned = 0
    for i in borrowed:
        if i[2] == name:
            booksBorrowed += 1
    for i in returned:
        if i[2] == name:
            booksReturned += 1
    outstandingBooks = booksBorrowed - booksReturned
    return outstandingBooks

#Returns an int of the amount owed by the person
def getOutstandingFines (name):
    amountOwed = 0
    for i in outstandingFines:
        if i[0] == name:
            amountOwed = i[1]
    return amountOwed

#Returns True or False to answer the question of "Can <user> borrow <book> on <day>?"
def canUserBorrowReqBook():

    #Creates a fake entry for the Borrow(<entry>) method
    tempEntry = []
    tempEntry.append("B")
    tempEntry.append(day)
    tempEntry.append(user)
    tempEntry.append(reqBook)
    tempEntry.append(reqBorrowLen)
    
    #Uses tempEntry to see if the person could successfuly borrow the book
    canBorrowBook = canBorrow(tempEntry)
    return canBorrowBook

#Looks through everyone with outstanding fines and returns the person with the most in the form [<Person's Name>, <Amount Owed>]
def getMostOutstandingFines():
    currentFines = 0
    currentName = ""
    maxFines = 0
    maxName = ""

    for i in outstandingFines:
        currentName = i[0]
        currentFines = i[1]
        if currentFines > maxFines:
            maxFines = currentFines
            maxName = currentName
    
    outputPerson = []
    outputPerson.append(maxName)
    outputPerson.append(maxFines)
    return outputPerson

    

#########################################################    MAIN CODE    ###########################################################
books = open("booklist-2.txt", "r")
log = open("librarylog-3.txt", "r")

day = int(input("What day is it: "))
reqBorrowLen = int(input("How many days are they borrowing for?: "))
reqBook = input("What book is it: ")
user = input("Who is requesting a book: ")

# sorting into lists 
# getting rid of the \n 
booklist = []
libLog = []
bookBorrowCounter = [] #bookBorrowCounter tracks the total number of days each book was borrowed for
totalCopiesPerBook = []
totalCopiesCounter = []
usageRatios = []

for x in books:
    if(x[-1:] == "\n"):
        y = x[:-1]
    elif(x[-1:] != "\n"):
        y = x
    y = y.split("#")
    y[1] = int(y[1])
    booklist.append(y)

#Put the starting books into bookBorrowCounter[] in format [<Book Name>, <Days borrowed>]
for x in booklist:
    newEntry = []
    newEntry.append(x[0])
    newEntry.append(0)
    bookBorrowCounter.append(newEntry)

# Puts the initial values in for totalCopiesPerBook[] (The book name and the number of copies for that book)
setTotalCopiesPerBook()
setTotalCopiesCounter()
    
#Fills out booklist and liblog
for x in log:
    if(x[-1:] == "\n"):
        y = x[:-1]
    elif(x[-1:] != "\n"):
        y = x
    y = y.split("#")
    if len(y) > 1:
        y[1] = int(y[1])
    libLog.append(y)

books.close()
log.close()

#Format: B#<day>#<Student Name>#<Book name>#<days borrowed for>
borrowed = []

#Format: R#<day>#<Student Name>#<Book name>
returned = []

#Format: A#<day>#<Book name>
newBooks = []

#Format: [<Student Name>, <Amount Owed>]
outstandingFines = []
mostFines = []

#Format: P#<day>#<student name>#<amount>
payedFines = []

#Fine Checker
#make a list of books that were borrowed
#make a list of books that were returned

#Run through the liblog and update information in real time going line-by-line
#The current day variable can be used to get the answers to questions that use the specific day as an input
dayCounter = int(libLog[0][1])
lastDay = int(libLog[len(libLog)-1][0])
currentLineDay = -1
lineNum = 0

while currentLineDay < lastDay-1 and dayCounter < lastDay-1:
    currentLineDay = int(libLog[lineNum][1])
    nextLineDay = int(libLog[lineNum+1][1])

    if dayCounter == 30:
        print("", end = "")

    if nextLineDay > currentLineDay:
        if(libLog[lineNum][0] == "B"):
            Borrow(libLog[lineNum])
        elif(libLog[lineNum][0] == "R"):
            Return(libLog[lineNum])
        elif(libLog[lineNum][0] == "A"):
            Addition(libLog[lineNum])
        elif(libLog[lineNum][0] == "P"):
            Fine(libLog[lineNum])
        dayCounter = currentLineDay
        while dayCounter < nextLineDay:
            if day == dayCounter:  
                mostFines = getMostOutstandingFines()
                borrowSuccessful = canUserBorrowReqBook()
            updateBookBorrowCounter()
            updateTotalCopiesCounter()
            dayCounter += 1

    
    if nextLineDay == currentLineDay:
        if(libLog[lineNum][0] == "B"):
            Borrow(libLog[lineNum])
        elif(libLog[lineNum][0] == "R"):
            Return(libLog[lineNum])
        elif(libLog[lineNum][0] == "A"):
            Addition(libLog[lineNum])
        elif(libLog[lineNum][0] == "P"):
            Fine(libLog[lineNum])
    
    lineNum += 1

#Looks at last day in libLog
currentLineDay = int(libLog[lineNum][1])
while lineNum < len(libLog)-1:
    currentEntry = libLog[lineNum]
    if(libLog[lineNum][0] == "B"):
        Borrow(libLog[lineNum])
    elif(libLog[lineNum][0] == "R"):
        Return(libLog[lineNum])
    elif(libLog[lineNum][0] == "A"):
        Addition(libLog[lineNum])
    elif(libLog[lineNum][0] == "P"):
        Fine(libLog[lineNum])

    lineNum += 1

if day == dayCounter:
    mostFines = getMostOutstandingFines()
    borrowSuccessful = canUserBorrowReqBook()
    alreadyCheckedQuestions = True
updateBookBorrowCounter()
updateTotalCopiesCounter()
setUsageRatio()




#################################################   Preparing OUTPUT   ######################################################

sort2DArray(usageRatios)
sort2DArray(outstandingFines)
sort2DArray(bookBorrowCounter)

print("OUTPUT: \n\n")



#################################################   OUTPUT/ANSWERS  ####################################################################



#checks user is able to borrow reqBook on day
if borrowSuccessful == True:
    print("Can", user,"borrow", reqBook,"on day", day, " for", reqBorrowLen, "days? Yes")
else:
    print("Can", user,"borrow", reqBook,"on day", day, " for", reqBorrowLen, "days? No")

# Prints books that were borrowed for the most and second most number of days
print("The book which was borrowed the most number of days is", bookBorrowCounter[len(bookBorrowCounter)-1][0], "and it was borrowed for", bookBorrowCounter[len(bookBorrowCounter)-1][1], "days")
print("The book which was borrowed the second most number of days is", bookBorrowCounter[len(bookBorrowCounter)-2][0], "and it was borrowed for", bookBorrowCounter[len(bookBorrowCounter)-2][1], "days")


# Prints the book with the highest, 2nd highest, and 5th highest usage ratios.
print("The book with the highest usage ratio is", usageRatios[len(usageRatios)-1][0], "with percentage", usageRatios[len(usageRatios)-1][1])
print("The book with the second highest usage ratio is", usageRatios[len(usageRatios)-2][0], "with percentage", usageRatios[len(usageRatios)-2][1])
print("The book with the fifth highest usage ratio is", usageRatios[len(usageRatios)-5][0], "with percentage", usageRatios[len(usageRatios)-5][1])


#Prints the person with the highest fine
print("The person with the highest fine is", outstandingFines[len(outstandingFines)-1][0], "with fine", outstandingFines[len(outstandingFines)-1][1])
outstandingFines.pop()

# Prints the two people with the second highest fine
print("The two people tied for the 2nd highest fine are named", outstandingFines[len(outstandingFines)-1][0], end = "")
print(",", outstandingFines[len(outstandingFines)-2][0], "and their fine is", outstandingFines[len(outstandingFines)-1][1])
outstandingFines.pop()
outstandingFines.pop()

# Prints the only remaining person with a fine
print("The only other person with a fine is", outstandingFines[0][0], "with fine", outstandingFines[0][1])

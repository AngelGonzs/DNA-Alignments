import csv
import os
import sys

# Open the file here so that it gets re-written on every run
# Later on we append every single sequence of the input
# So that's why this is necessary
open("results.csv",'w')


# NOTE: To avoid any string encoding issues we use
# utf-8-sig. The main cause of this is because during
# debugging with csv files made in Excel, when drawing
# the scoring matrix I'd see a "ufeff" character
# with the utf encoding we avoid this ocurring



# INITIALIZES A TABLE WITH THE SEQUENCES AND GAP PENALTIES
# The parameters S1 and S2 are the sequences, d being the gap penalty
# What I mean by initializing it is just filling out the basic values
# Like the characters from the sequences and the Gap Penalty
# Later on we will fill up the entire table
def initialize(S1, S2, d):
    Table = []


    for i in range(columnLength):
        col = []
        for i in range(rowLength):
            col.append(" ")
        Table.append(col)
    # Create table with empty values

    for i in range(len(S1)):
        Table[0][i + 2] = S1[i]

    for i in range(len(S2)):
        Table[i + 2][0] = S2[i]

    # Filling up the variables for S1 and S2

    # Time to add the Gap Penalties

    # Penalties Start at [1][1]

    for i in range(1, rowLength):
        Table[1][i] = d * (i - 1)

    for j in range(1, columnLength):
        Table[j][1] = d * (j - 1)

    return Table


# First parameter, having the match/mismatch scores
# and the gap penalty as the rest of our parameters
# We will fully fill the table with it's score
# and be able to get the alignment score
def scoringMatrix(Table, match, mismatch, d):
    # We are give match = 1 and mismatch = -1

    for i in range(2, columnLength):

        for j in range(2, rowLength):

            if Table[i][0] == Table[0][j]:
                score = match
            else:
                score = mismatch

            Table[i][j] = max(Table[i - 1][j - 1] + score, Table[i][j - 1] + d, Table[i - 1][j] + d)

    return Table


# IN THIS METHOD WE DO THE BACKTRACKING AND GET THE ALIGNMENT TEXT FOR OUR SEQUENCES

# NOTE: IF YOU WANT TO VERIFY THE BACKTRACKING JUST ADD A PRINT IN THE
# BOTTOM CORNER AND PRINT THE MAXIMUM ON EACH ITERATION

# Here we just do the backtracking to get the alignment.
# If wanted, you could save all the max values in each
# Iteration into an array and that would be the backtracking
# values, or just print them as it is said above

# The parameter here is just a filled Table, a scored Matrix
def alignment(Table):
    # We start the search from our Alignment Score (Bottom Right Corner]

    # We check which of our surrounding values is greater than the current value
    # Move into that block and verify if A and B match. Repeat process
    i = rowLength - 1
    j = columnLength - 1
    alignmentText = ""

    if Table[0][i] == Table[j][0]: alignmentText += Table[j][0]
    # Check bottom corner

    while True:

        if i <= 2 or j <= 2:
            break

        # We check:
        # Table[j-1][i]  (left to the bottom right)     MAX1
        # Table[j][i-1]  (upper to bottom right)        MAX2
        # Table[j-1][i-1] (Diagonal)                    MAX3

        maximum = max(Table[j - 1][i], Table[j][i - 1], Table[j - 1][i - 1])

        # print(maximum)
        # un-comment this print to check out backtracking

        if maximum == Table[j - 1][i - 1]:

            if Table[j - 1][0] == Table[0][i - 1]:
                # print("MAX3", Table[j - 1][0])

                alignmentText += Table[j - 1][0]

            else:
                alignmentText += "-"
            i -= 1
            j -= 1

        elif maximum == Table[j][i - 1]:
            # Check if A and B match
            if Table[0][i - 1] == Table[j][0]:
                # MATCH!
                # print("MAX1", Table[0][i - 1])

                alignmentText += Table[0][i - 1]

            else:
                alignmentText += "-"
            i -= 1

        elif maximum == Table[j - 1][i]:

            if Table[j - 1][0] == Table[0][i]:
                # print("MAX2", Table[0][i])

                alignmentText += Table[0][i]

            else:
                alignmentText += "-"
            j -= 1

    # FOR THE TEXT TO BE CORRECT WE HAVE TO REVERSE IT SINCE
    # IN THIS IMPLEMENTATION WE SEARCH WHILE BACKTRACKING

    resultText = ""

    for i in range(len(alignmentText) - 1, -1, -1):
        resultText += alignmentText[i]

    return resultText


# HERE IS WHERE THE CALLS START
# WE INITIALIZE X AS A COMMAND LINE ARGUMENT AND
# THEN GIVE IT AS THE FILENAME SO THAT WE CAN ABSTRACT THE PATH

x = sys.argv[1]
fileName = os.path.abspath(x)


with open(fileName, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        S1, S2 = line

        rowLength = len(S1) + 2
        columnLength = len(S2) + 2

        # CREATE AN INITIALIZED ARRAY WITH A GAP PENALTY OF -2:
        Table = initialize(S1, S2, -2)


        # SCORE THE ARRAY ABOVE:
        scoredMatrix = scoringMatrix(Table, 1, -1, -2)

        # print("\nScored Matrix SEX: ")
        # for array in scoredMatrix:
        #     print(array)

        # With files of smaller input the above statement
        # can be uncommented to check the scoring matrix
        # not rly the case with files of such big input
        # since the terminal wont be able to format it well


        # Get the alignment of the scored Matrix
        alignmentText = alignment(scoredMatrix)


        alignmentScore = scoredMatrix[columnLength-1][rowLength-1]
        # i messed up the column and row variables, my bad but it works we just have to imagine them inverse :)


        resultArray = [S1, S2, S1 + "\n" + alignmentText, alignmentScore, " "]

        # S1 repeated to put the file into
        # ATGCT
        # A-GCT
        # Format

        # At the end of the array we add a blank space, this is solely
        # for readability in the results.csv file

        # Now we have all the required elements to write into the results.csv file
        # So all that's left is to write the file


        with open("results.csv", 'a') as new_file:
            csv_writer = csv.writer(new_file)

            for line in resultArray:
                csv_writer.writerow([line])




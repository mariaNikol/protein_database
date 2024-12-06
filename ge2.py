import mysql.connector as mysql
import datetime
import string

def print_menu():
    print ('1. Δημιουργία/Διαγραφή Πίνακα')
    print ('2. Εισαγωγή νέας πρωτεΐνης')
    print ('3. Διαγραφή όλων των πρωτεϊνών')
    print ('4. Αναζήτηση με βάση την πρωτεϊνική ακολουθία')
    print ('5. Αναζήτηση πρωτεϊνών ανά έτος καταχώρησης')
    print ('6. Αναζήτηση πρωτεϊνών ανά οργανισμό')
    print ('7. Έξοδος')

#δημιουργία set για τον έλεγχο των ακολουθιών
latins = set(string.ascii_lowercase)
latins = latins.union(set(string.ascii_uppercase))

#A
#φτιάχνει connection object
proteindb_connection = mysql.connect(host = "localhost",user="root",passwd="",db="menu")
#φτιάχνει cursor
newcursor = proteindb_connection.cursor()

user_inp=0
#αν το input του χρήστη είναι 7 διακόπτεται η while
#αν είναι μεταξύ 1-6 κάνει τις αντίστοιχες ενέργειες
#αν ειναι οτιδήποτε άλλο εκτυπώνει ξανά το μενού
while user_inp!= '7':
    print_menu()
    user_inp = input("Επιλογή:")
#Β δημιουργείται ένας νέος πίνακας Proteins στην τοπική βάση
    if (user_inp == '1' ):
        #αν υπάρχει ο πίνακας τον διαγράφει
        newcursor.execute("DROP TABLE IF EXISTS Proteins")
        #query για τον νεο πίνακα με τα πεδια που πρέπει να έχει
        create_table_proteins = """
        CREATE TABLE Proteins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            protein_name VARCHAR(500),
            protein_sequence VARCHAR(500),
            sequence_length INT,
            year INT,
            organism VARCHAR(500),
            data_source VARCHAR(500)
        )
        """
        newcursor.execute(create_table_proteins) #εκτελεί τη δημιουργία πίνακα
        proteindb_connection.commit() #κάνει commit τις αλλαγές
        print ("----------------------------\n")
#Γ εισαγωγή νεας πρωτεϊνης
    elif (user_inp == '2' ):
        try: #έλεγχος για τον τύπο δεδομένων      
            print ('2. Εισαγωγή νέας πρωτεΐνης \n')
            #input για τα πεδια του πίνακα
            protein_name = str(input("Όνομα Πρωτεϊνης: "))
            while True: #έλεγχος για τη χρονιά, αν ειναι μετά την τρέχουσα ζητάει ξανά input
                year = int(input("Έτος καταχώρησης: "))
                if year > datetime.datetime.now().year:
                    print("Το έτος δεν μπορει να είναι μετά την τρέχουσα χρονιά! Δοκιμάστε ξανά")
                else:
                    break
            while True: #έλεγχος για την ακολουθία, αν περιέχει χαρακτήρες εκτός των λατινικών γραμματων ζητάει ξανά την ακολουθία
                sequence = str(input("Ακολουθία: "))
                if set(sequence).issubset(latins):
                    break
                else:
                    print ("H ακολουθία πρέπει να περιέχει μόνο αμινοξέα! Δοκιμάστε ξανά")         
            while True: #έλεγχος για τον οργανισμό, αν περιέχει αριθμούς ζητάει ξανά input
                organism = str(input("Οργανισμός: "))
                if any(char.isdigit() for char in organism):
                    print (" Ο οργανισμός δεν επιτρέπεται να περιέχει αριθμούς! Δοκιμάστε ξανα")
                else:
                    break
            while True: #έλεγχος για την πηγή δεδομένων, αν περιέχει αριθμούς ζητάει ξανά input
                data_source = str(input("Πηγή Δεδομένων: "))
                if any(char.isdigit() for char in data_source):
                    print (" H πηγή δεν επιτρέπεται να περιέχει αριθμούς! Δοκιμάστε ξανα")
                else:
                    break
           
            insert_protein = """
            INSERT INTO Proteins (protein_name, protein_sequence, sequence_length, year, organism, data_source)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            newcursor.execute(insert_protein,(protein_name,sequence,len(sequence),year,organism,data_source))

            newcursor.execute ("""SELECT * FROM Proteins""")
            for x in newcursor: #εκτυπώνει τα περιεχόμενα για επιβεβαίωση σωστής καταχώρησης
                print(x)
            proteindb_connection.commit()
            print("----------------------------\n")
        except ValueError as e:
            print("Η πρωτεϊνη δεν καταχωρήθηκε λόγω λάθους τύπου δεδομένων.")
#Δ διαγράφει όλες τις εγγραφές του πίνακα Proteins αφού λάβει επιβεβαίωση
    elif (user_inp =='3' ):
        print ('3. Διαγραφή όλων των πρωτεϊνών \n')
        r_u_sure = input("Θέλετε να διαγράψετε όλα τα περιεχόμενα? (y or n) ")
        if r_u_sure == "y":
            newcursor.execute("DELETE FROM Proteins")
            proteindb_connection.commit()
            print("H διαγραφή ολοκληρώθηκε")
            print("----------------------------\n")
        else:
            print("Η διαγραφή ΔΕΝ ολοκληρώθηκε")
            print("----------------------------\n")
#Ε  χρήστης δίνει ένα κομμάτι πρωτεϊνικής ακολουθίας ως είσοδο στο πρόγραμμα και το πρόγραμμα εμφανίζει όλα τα πεδία των
# αντίστοιχων εγγραφών αν υπάρχουν διαφορετικά εκτυπώνει ότι δεν βρέθηκαν αποτελέσματα
    elif (user_inp =='4' ):
        find_seq_str = input("Aκολουθία για αναζήτηση: ")
        newcursor.execute("""
            SELECT * FROM Proteins
            WHERE protein_sequence LIKE %s
        """, (f"%{find_seq_str}%",))
        results = newcursor.fetchall()
        if results:
            print("SEARCH RESULTS:")
            for x in results:
                print(x)
        else:
            print("Δε βρέθηκαν αποτελέσματα.")
        print("\n")
#ΣΤ εμφανίζει όλες τις πρωτεΐνες που καταχωρήθηκαν σε ένα συγκεκριμένο έτος     
    elif (user_inp =='5' ):
        find_year = input("Έτος για αναζήτηση: ")
        newcursor.execute("""
            SELECT * FROM Proteins
            WHERE year = %s
        """, (find_year,))
        results = newcursor.fetchall()
        if results:
            print("SEARCH RESULTS:")
            for x in results:
                print(x)
        else:
            print("Δε βρέθηκαν αποτελέσματα.")
        print("\n")
#Ζ εμφανίζει όλες τις πρωτεΐνες ενός συγκεκριμένου οργανισμού με μήκος ακολουθίας μεταξύ 5 και 10           
    elif (user_inp =='6' ):
        organismos = input("Οργανισμός για αναζήτηση: ")
        newcursor.execute("""
            SELECT * FROM Proteins
            WHERE  organism = %s AND sequence_length >= 5 AND sequence_length <= 10 
        """, (organismos,))
        results = newcursor.fetchall()
        if results:
            print("SEARCH RESULTS:")
            for x in results:
                print(x)
        else:
            print("Δε βρέθηκαν αποτελέσματα.")
        print("\n")
    else:
        print('Επιλέξτε απο τα παρακάτω')
        print_menu()
    
proteindb_connection.commit()
proteindb_connection.close()

    

# Console impelementation of ASK.FM

import sqlite3

# connect the data base
conn = sqlite3.connect('data.db')
db = conn.cursor()

# global variable to detect the current user
Current_User = ""

def OnStart():
    # get user's input
    Choice = input("\nChoose:\n\t\t1) Log In \n\t\t2) Sign Up\nOperation: ")
    
    # check for Invalid input
    try:
        Operation = int(Choice)
        if Operation == 1 or Operation == 2:
            return Operation
        else:
            print("\n!!!!Invalid choice, please try again!!!!")
            return 3
    except:
        print("\n!!!!Invalid choice, please try again!!!!")
        return 3


def LogIn():
    # refere to current user
    global Current_User
    
    # check the username and password in the data base
    user_name = input("\nUsername: ")
    password = input("Password: ")
    db.execute("SELECT * FROM users")
    users = db.fetchall()
    found = False
    
    for user in users:
        if user[1] == user_name:
            if user[2] == password:
                found = True
                Current_User = user_name
                break
    
    # if wrong username or password return to the start menu
    if not found:
        print("\n!!!!Wrong username or password!!!!")
        return OnStart()

    # if LogIn successfully return 0 to the main
    return 0


def SignUp():
    # refere to current user
    global Current_User

    # get user's data
    User_name = input("\nUsername: ")
    E_Mail = input("E-mail: ")
    Password = input("Password: ")
    Confirm_Password = input("Confirm password: ")
    Ask_Anonymously = input("Allow anonymous questions: ")
    
    # check if the username already exist
    db.execute("SELECT * FROM users")
    users = db.fetchall()
    Not_Exist = True
    for user in users:
        if user[1] == User_name:
            Not_Exist = False
            break
    
    if not Not_Exist:
        print("\n!!!!The username already exist!!!!")
        return OnStart()
    
    # check the password
    if Password != Confirm_Password:
        print("\n!!!!The password does not match!!!!")
        return OnStart()

    # check anonymous questions
    if Ask_Anonymously == 1 or Ask_Anonymously.lower() == "y" or Ask_Anonymously.lower() == "yes":
        Ask_Anonymously = 1
    elif Ask_Anonymously == 0 or Ask_Anonymously.lower() == "n" or Ask_Anonymously.lower() == "no":
        Ask_Anonymously = 0

    # if SignUp successfully add the user to the data base
    db.execute("INSERT INTO users (user_name, password, e_mail, ask_anonymously) VALUES (?, ?, ?, ?)", (User_name, Password, E_Mail, Ask_Anonymously))
    conn.commit()
    Current_User = User_name
    return 0 

def LogOut():
    # refere to current user
    global Current_User

    Current_User = ""

def Menu():
    # print the operations
    print("\nMenu")
    print("\t\t1) Print Questions To Me")
    print("\t\t2) Print Questions From Me")
    print("\t\t3) Answer Question")
    print("\t\t4) Delete Question")
    print("\t\t5) Ask Question")
    print("\t\t6) List System Users")
    print("\t\t7) Feed")
    print("\t\t8) LogOut")

    # get user's input
    Choice = input("Operation: ")
    
    # check for Invalid input
    try:
        Operation = int(Choice)
        if Operation in range(1,9):
            return Operation
        else:
            print("\n!!!!Invalid choice, please try again!!!!")
            return 9
    except:
        print("\n!!!!Invalid choice, please try again!!!!")
        return 9

def QuestionsToME():
    # refere to current user
    global Current_User
    
    # get questions from the data base
    db.execute("SELECT * FROM questions WHERE (receiver=? AND deleted=0)",(Current_User,))
    Questions = db.fetchall()

    # print the questions
    for question in Questions:
        # check if the question is part of a thread or not
        thread = False
        if question[5] != -1:
            print("\nThread: ", end="")
            thread = True
        
        #print question Id and the sender
        if not thread:
            print("\n", end="")
        print(f"Question Id({question[0]}) from {question[1]}: ", end="\t\t")

        #print question and answer
        print(f"Question: {question[3]} ", end="\t\t")
        
        if question[4] != "None":
            print(f"Answer: {question[4]}")
        elif question[4] == "None":
            print()

def QuestionsFromME():
    # refere to current user
    global Current_User
    
    # get questions from the data base
    db.execute("SELECT * FROM questions WHERE (sender=? AND deleted=0)",(Current_User,))
    Questions = db.fetchall()

    # print the questions
    for question in Questions:
        # chaeck for anonymous question
        db.execute("SELECT * FROM users WHERE (user_name=?)",(question[2],))
        receiver = db.fetchall()
        AQ = True
        if receiver[0][4] == 0:
            AQ = False

        # check if the question is part of a thread or not
        thread = False
        if question[5] != -1:
            print("\nThread: ", end="")
            thread = True
        
        #print question Id and the receiver
        if not thread:
            print("\n", end="")
        print(f"Question Id({question[0]}) ", end="")
        if not AQ:
            print("!AQ ", end="")
        print(f"to {question[2]}:", end="\t\t")

        #print question and answer
        print(f"Question: {question[3]}", end="\t")
        
        if question[4] != "None":
            print(f"Answer: {question[4]}")
        elif question[4] == "None":
            print("Not Answered YET")

def AnswerQuestion():
    # refere to current user
    global Current_User
    
    # get question id and the answer
    question_id = input("\nEnter question Id or -1 to cancel: ")

    # check question id
    try:
        question_id = int(question_id)
        if question_id == -1:
            return -1
    except:
        print("\n!!!!Invalid input, please try again!!!!")
        return 9 

    # check if the question exist or not
    db.execute("SELECT question_id FROM questions")
    QuestionID = db.fetchall()
    
    ID_Exist = False
    for id in QuestionID:
        if id[0] == question_id:
            ID_Exist = True
            break
    
    if not ID_Exist:
        print("\n!!!!Invalid input, please try again!!!!")
        return 9

    # get the question from the data base
    db.execute("SELECT * FROM questions WHERE question_id=?",(question_id,))
    Question = db.fetchall()

    # check if the question belongs to that user
    if Question[0][2] != Current_User:
        print("\n!!!!Invalid input, please try again!!!!")
        return 9

    # check if question had been deleted
    if Question[0][6] == 1:
        print("\n!!!!Invalid input, please try again!!!!")
        return 9

    # view question information
    print(f"Question Id ({Question[0][0]}) from {Question[0][1]}:", end="\t\t")
    print(f"Question: {Question[0][3]}")
    
    # check if question had been answered before
    if Question[0][4] == "None":
        answer = input("Answer: ")
    else:
        print("!!!!Warning: already answered. Answer will be updated!!!!")
        answer = input("Answer: ")

    # update the answer
    db.execute("UPDATE questions SET (answer) = (?) WHERE question_id=? ", (answer, question_id))
    conn.commit()

    # the answer updated successfully
    return 0

def DeleteQuestion():
    # refere to current user
    global Current_User

    # get question id
    question_id = input("\nEnter question Id or -1 to cancel: ")

    # check question id
    try:
        question_id = int(question_id)
        if question_id == -1:
            return -1
    except:
        print("\n!!!!Invalid choice, please try again!!!!")
        return 9

    # check if the question exist or not
    db.execute("SELECT question_id FROM questions")
    QuestionID = db.fetchall()
    
    ID_Exist = False
    for id in QuestionID:
        if id[0] == question_id:
            ID_Exist = True
            break
    
    if not ID_Exist:
        print("\n!!!!Invalid input, please try again!!!!")
        return 9

    # get the question from the data base
    db.execute("SELECT * FROM questions WHERE question_id=?",(question_id,))
    Question = db.fetchall()

    # check if the question belongs to that user
    if Question[0][2] != Current_User:
        print("\n!!!!Invalid choice, please try again!!!!")
        return 9

    # check if the question had been deleted before
    if Question[0][6] != Current_User:
        print("\n!!!!The question had been deleted before!!!!")
        return 9

    # delete the question
    db.execute("UPDATE questions SET (deleted) = (1)")
    conn.commit()

    # the question deleted successfully
    return 0

def AskQuestion():
    # refere to current user
    global Current_User

    user_id = input("\nEnter user id or -1 to cancel: ")
    
    # check user id
    try:
        UserId = int(user_id)
        if UserId == -1:
            return -1
    except:
        print("\n!!!!Invalid choice, please try again!!!!")
        return 9
    
    # check if the user exist or not
    db.execute("SELECT user_id FROM users")
    User_ID = db.fetchall()
    
    ID_Exist = False
    for id in User_ID:
        if id[0] == UserId:
            ID_Exist = True
            break
    
    if not ID_Exist:
        print("\n!!!!Invalid input, please try again!!!!")
        return 9

    # load the reciver user data
    db.execute("SELECT * FROM users Where user_id==?", (UserId,))
    user = db.fetchall()
    
    # check if that user allowes anonymous qusetions
    if user[0][4] == 0: 
        print("NOTE: anonymous questions are not allowed for this user")

    thread_id = input("For thread questions: Enter question id or -1 for new question: ")

    #check thread id     
    try:
        thread_id = int(thread_id)
        
        # get the qustion
        Question = input("Enter question text: ")
        
        if thread_id == -1:
            # new question
            db.execute("INSERT INTO questions (sender, receiver, question, answer, head_question, deleted) VALUES (?,?,?,'None', -1, 0)",(Current_User, user[0][1], Question))
            conn.commit()

            # the question added successfully
            return 0

        else:
            # thread question
            db.execute("INSERT INTO questions (sender, receiver, question, answer, head_question, deleted) VALUES (?,?,?,'None', ?, 0)",(Current_User, user[0][1], Question, thread_id))
            conn.commit()

            # check if that thread exists or creat new one
            db.execute("SELECT * FROM threads")
            threads = db.fetchall()
            Not_Exist = True
            for thread in threads:
                if thread[0] == thread_id:
                    Not_Exist = False
                    break
            
            if Not_Exist:
                db.execute("INSERT INTO threads (head_qustion, deleted) VALUES (?, 0)",(thread_id))
                conn.commit()

            # the tread added successfully
            return 0

    except:
        db.execute("INSERT INTO threads (head_qustion, deleted) VALUES (?, 0)",(thread_id,))
        conn.commit()
        print("\n!!!!Invalid choice, please try again!!!!")
        return 9

def ListSystemUsers():
    # get users data
    db.execute("SELECT * FROM users")
    users = db.fetchall()
    print()

    # view system users
    for user in users:
        print(f"ID: {user[0]}\tName: {user[1]}")

def Feed():
    # get questions from the data base
    db.execute("SELECT * FROM questions WHERE (deleted=0)")
    Questions = db.fetchall()

    # print the answered questions
    for question in Questions:
        # check if question has been answered
        if question[4] == "None":
            continue

        # chaeck for anonymous question
        db.execute("SELECT * FROM users WHERE (user_name=?)",(question[2],))
        receiver = db.fetchall()
        AQ = True
        if receiver[0][4] == 0:
            AQ = False

        # check if the question is part of a thread or not
        thread = False
        if question[5] != -1:
            print(f"\nThread Parent Question ID({question[5]}) ", end="")
            thread = True
        
        #print question Id, the sender, and the receiver
        if not thread:
            print("\n", end="")
        print(f"Question Id({question[0]}) ", end="")
        if not AQ:
            print("!AQ ", end="")
        print(f"from {question[1]} to {question[2]}:", end="\t\t")

        #print question and answer
        print(f"Question: {question[3]}", end="\t")
        print(f"Answer: {question[4]}")
            
def RunAsk():
    Operation = Menu()
    while True:
        # select operations
        if Operation == 1:
            QuestionsToME()
            input()
            Operation = Menu()
            continue

        elif Operation == 2:
            QuestionsFromME()
            input()
            Operation = Menu()
            continue

        elif Operation == 3:
            Choice = AnswerQuestion()
            if Choice == 0 or Choice == -1:
                Operation = Menu()
                continue
            else:
                Operation = Menu()
                continue

        elif Operation == 4:
            Choice = DeleteQuestion()
            if Choice == 0 or Choice == -1:
                Operation = Menu()
                continue
            else:
                Operation = Menu()
                continue

        elif Operation == 5:
            Choice = AskQuestion()
            if Choice == 0 or Choice == -1:
                Operation = Menu()
                continue
            else:
                Operation = Menu()
                continue

        elif Operation == 6:
            ListSystemUsers()
            input()
            Operation = Menu()
            continue

        elif Operation == 7:
            Feed()
            input()
            Operation = Menu()
            continue

        elif Operation == 8:
            LogOut()
            Start()
            Operation = Menu()
            continue


def Start():
    # Start screen
    Operation = OnStart()
    
    # LogIn or SignUp
    while Operation != 0:
        # LogIn
        if Operation == 1:
            Operation = LogIn()
        
        # SignUp
        elif Operation == 2:
            Operation = SignUp()
        
        # for Inavlid input
        else:
            Operation = OnStart()

def main():
    # start the applicatin for LogIn and SignUp
    Start()

    # run the application after SignUp or LogIn
    RunAsk()

# Call the main function to run the project
main()
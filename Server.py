import socket, threading
import questionBank
import random
import re
import io
from contextlib import redirect_stdout



class ClientThread(threading.Thread):


    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        self.msg = ""
        self.questionId = 0
        self.score = 0
        print("New connection added: ", self.clientAddress)


    def run(self):
        print("Connection from : ", self.clientAddress)
        self.getQuestion()
        self.csocket.send(self.msg)

        while True:
            data = self.csocket.recv(1024)
            self.msg = data.decode()
            if (self.msg == "exit"):     #Terminate the connection
                self.msg = ("bye").encode()
                self.csocket.send(self.msg)
                break
            elif (self.msg == "skip"):     #To get another question
                self.getQuestion()
                self.csocket.send(self.msg)
            elif (self.msg == "Overall"):   #To get the overall line as a string seperated
                message = "Overall Score: "+str(self.score)+ "%"
                self.msg = message.encode()
                self.csocket.send(self.msg)
            else:
                self.evaluateFunction()     #To evaluate the function based on the input(s) and output(s) in case there is return
                self.csocket.send(self.msg)

        print("Client at ", self.clientAddress, " disconnected...")


    def evaluateFunction(self):
        self.score = 0
        testCaseInputs = q.getInputOfTestCases(str(self.questionId))    #getting all the inputs of the question
        testCaseOutput = q.getOutputOfTestCases(str(self.questionId))   #getting all the outputs of the question
        withOutput = q.fetchOneRowOfQuestionTable(str(self.questionId)) #If the question with output or not
        expression = r"(def \w+)"
        a = re.match(expression, self.msg).group(0)  #To take the name of the function the user provided
        a = a.split()
        a = a[1]    #a has the function name
        methodName = re.search(a,withOutput[1])    #checking if the name of the function same as the one in the question
        if(methodName != None):
            message = []
            rowResult = ""
            # case the function without return
            if(str(withOutput[3]) == "0"):
                if (testCaseInputs != None):
                    j=0
                    try:
                        exec(self.msg)    #executing the string the user provided
                        for expected in testCaseOutput:
                            tempInput = testCaseInputs[j]
                            temp = a + tempInput[0]
                            with io.StringIO() as buf, redirect_stdout(buf):   #To take the output from the buffer
                                try:
                                    eval(temp)     # Evaluating the function with the inputs
                                except Exception as e:
                                    rowResult = str(e) + "\n"   #If there is any mistake
                                    break
                                output = buf.getvalue()
                            output = output.strip()
                            rowResult = rowResult + "Test Case " + str(j + 1) + "= " + str(output)
                            if(str(output) == str(expected[0]) ):
                                self.score = self.score + 1    #calculating the score
                                rowResult = rowResult + " TRUE \n"
                            else:
                                rowResult = rowResult + " FALSE\n"
                            j = j+1
                    except Exception as e:
                        rowResult = rowResult + str(e) + "\n"     #Providing the Error of the function the uesr wrote
                else:
                    print("Error...")
            # case the function with return
            elif (str(withOutput[3]) == "1"):
                if (testCaseInputs != None):
                    j=0
                    try:
                        exec(self.msg)
                        for expected in testCaseOutput:
                            tempInput = testCaseInputs[j]
                            rowResult = rowResult + "Test Case "+str(j+1)+":" + str(tempInput[0]) + "= "
                            temp = a + tempInput[0]
                            try:
                                res = eval(temp)
                            except Exception as e:
                                rowResult =  str(e) + "\n"
                                break

                            if(str(res) == str(expected[0]) ):
                                rowResult = rowResult + str(expected[0]) + " TRUE\n"
                                self.score += 1  #calculating the score
                            else:
                                rowResult = rowResult + str(expected[0]) + " FALSE\n"
                            j = j+1
                    except Exception as e:
                        rowResult = rowResult + str(e) + "\n"
                else:
                    rowResult = "Error..\n"
            else:
                rowResult = "Error..\n"
        else:
            rowResult = "The name of the function is not correct!!\n"

        self.score = (self.score * 100) / len(testCaseOutput)
        self.msg = (str(rowResult)).encode()   #in order to send the result


    def getQuestion(self):
        rows = q.fetchAllRowsOfQuesitonTable()    #getting all the question to choose one of the them
        numberOfQuesitons = len(rows)

        self.questionId = random.randrange(numberOfQuesitons)   #Randomly choosing the question to display
        self.questionId += 1
        row = q.fetchOneRowOfQuestionTable(str(self.questionId))   #Fetching the randomly choosing one
        #print(row[1])                       #To get the description of the question
        self.msg = (row[1]).encode()


#main
q = questionBank.questionBank()
choice = '-1'
while (choice != '0'):
    print("1. Administration mode")
    print("2. Running mode")
    print("0. Exit")
    choice = input("Enter your choice: ")
    print("\n")
    #Administration mode
    if (choice == '1'):
        print("1. Add a new question")
        print("2. Update an existing question")
        print("3. Add a new test case")
        print("4. Update an existing test case")
        print("5. Delete an existing test case")
        print("0. Exit")
        choice = input("Enter your choice: ")
        print("\n")
        print("\n")
        if (choice == '1'):
            q.craeteDataBase()   #Create the database in case it is not created
            while True:
                try:
                    id = int(input("Enter question id: "))
                    break
                except:
                    print("Invalid input, enter only numbers")

            description = input("Enter question description: ")
            flag = True
            while (flag):
                isActive = input("Is the question active(y/n)? ")
                if (isActive == "y" or isActive == "Y"):
                    isActive = 1
                    flag = False
                elif (isActive == "n" or isActive == "N"):
                    isActive = 0
                    flag = False
                else:
                    print("Invalid input, please re-enter")


            flag = True
            while (flag):
                withOutput = input("Is there output(y/n)? ")
                if (withOutput == "y" or withOutput == "Y"):
                    withOutput = 1
                    flag = False
                elif (withOutput == "n" or withOutput == "N"):
                    withOutput = 0
                    flag = False
                else:
                    print("Invalid input, please re-enter")
            #Adding the question
            q.insertINTOquestion(id, description, isActive, withOutput)

        elif (choice == '2'):

            rows = q.fetchAllRowsOfQuesitonTable()          #Display all the rows for the question table
            for row in rows:
                print("Qestion Id",row[0])
                print("Description ",row[1])
                print("Active/Deactive: "+ str(row[2]))
                print("With output?: "+ str(row[3]) + "\n")


            id = input("Enter the id of the question: ")           #Getting the id form the user
            row = q.fetchOneRowOfQuestionTable(id)                 #Fetching the question to be modified
            if(row != None):                                       #If the Id exists
                id = row[0]
                description = row[1]
                isActive = row[2]


                print("Question Id: ",id)
                print("Description: ", description)
                if(isActive == 1):
                    print("The question is active")
                    activation = "1. Deactivate? "           #To print wethear the quetions is active or not
                else:
                    print("The question is not active")
                    activation = "1. Activate? "

                print(activation)                           #To print wethear the quetions is active or not
                print("2. Update the description of the question: ")
                choice = input("Enter your choice: ")
                print("\n")

                if (choice == '1'):                         #changing the mode accordingly
                    if(row[2] == 1):
                        isActive = 0
                    else:
                        isActive = 1

                if (choice == '2'):                         #modyfing the description
                    description = input("Description: ")
                flag = True
                while (flag):
                    withOutput = input("Is there output(y/n)? ")
                    if (withOutput == "y" or withOutput == "Y"):
                        withOutput = 1
                        flag = False
                    elif (withOutput == "n" or withOutput == "N"):
                        withOutput = 0
                        flag = False
                    else:
                        print("Invalid input, please re-enter")
                q.updateQuestionTable(id, description, isActive, withOutput)
            else:                                           #Otherwise the Id is not in the table
                print("Invalid input, id not found")
            choice = '-1'                                   #go back to the main loop

        elif (choice == '3'):
            testCaseInput = ()


            rows = q.fetchAllRowsOfQuesitonTable()  # Display all the rows for the question table
            for row in rows:
                print("Qestion Id", row[0])
                print("Description: ", row[1])
                print("Active/Deactive: " + str(row[2]) + "\n")

            id = input("choose a qestion to add a test case for it")

            row = q.fetchOneRowOfQuestionTable(id)                 #Fetching the question to be modified
            if(row != None):                                       #If the Id exists
                numberOfInput = input("Enter the number of inputs")
                for i in range(int(numberOfInput)):
                    temp = input("Input number "+str(i+1) + ": ")
                    testCaseInput = testCaseInput + (int(temp),)

                testCaseOutput = input("Enter the output of the test case")

                q.insertINTOtestcase(id, str(testCaseInput), str(testCaseOutput))
            else:
                print("Invalid input, the recored was not found in question table")
                print('\n')

            choice = '-1'

        elif (choice == '4'):
            testCaseInput = ()
            rows = q.fetchAllRowsOfTestCaseTable()

            for row in rows:     #printing avilable test cases in order to modify one of them
                print("Test case Id: ",row[0])
                print("Test case input(s): ",row[1])
                print("Test case output: "+str(row[2]) + '\n' )


            print("Choose a test case to modify: ")
            id = input("Enter id: ")
            numberOfInput = input("Enter the number of inputs: ")
            for i in range(int(numberOfInput)):
                temp = input("Input number " + str(i + 1) + ": ")
                testCaseInput = testCaseInput + (int(temp),)

            row = q.fetchOneRowOfTestCaseTable(id,str(testCaseInput))
            if (row != None):
                print("\nTest case Id: ",row[0])
                print("Test case input(s): ",row[1])
                print("Test case output: "+str(row[2]) + '\n' )

                print("1. Update inputs: ")
                print("2. Update output: ")
                print("0. Exit")
                choice = input("Enter your choice")

                if (choice == '1'):
                    pass

                elif (choice == '2'):
                    testCaseOutput = input("Output: ")
                    q.updateTestCaseTable(id, str(testCaseInput), str(testCaseOutput))


            else:
                print("Invalid input, the recored was not found in test case table")

        elif (choice == '5'):

            testCaseInput = ()
            rows = q.fetchAllRowsOfTestCaseTable()

            for row in rows:  # printing avilable test cases in order to modify one of them
                print("Test case Id: ", row[0])
                print("Test case input(s): ", row[1])
                print("Test case output: " + str(row[2]) + '\n')

            print("Choose a test case to delete: ")
            id = input("Enter id: ")
            numberOfInput = input("Enter the number of inputs: ")
            for i in range(int(numberOfInput)):
                temp = input("Input number " + str(i + 1) + ": ")
                testCaseInput = testCaseInput + (int(temp),)

            row = q.fetchOneRowOfTestCaseTable(id, str(testCaseInput))
            if (row != None):
                print("The following record has been deleted")
                print("\nTest case Id: ", row[0])
                print("Test case input(s): ", row[1])
                print("Test case output: " + str(row[2]) + '\n')

                q.deleteTestCaseTable(id, str(testCaseInput))
                choice = '-1'

            else:
                print("Invalid input, the recored was not found in question table")

        else:
            choice = '-1'
        choice = '-1'
    #Running mode
    if (choice == '2'):
        HOST = "127.0.0.1"
        PORT = 5003
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        print("Server started")
        print("Waiting for client request..")

        while True:
            server.listen(1)
            clientsock, clientAddress = server.accept()
            newthread = ClientThread(clientAddress, clientsock)
            newthread.start()


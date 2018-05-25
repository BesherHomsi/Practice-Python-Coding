from tkinter import *
import tkinter.messagebox
import socket
import math
import questionBank
import re


class EntryDemo(Frame):


    def __init__(self, client):
        self.client = client
        self.in_data = ""
        self.recive()

        if self.in_data == "bye":
            raise ValueError
        else:
            self.GUI()


    def GUI(self):
        Frame.__init__(self)
        self.pack(expand=YES, fill=BOTH)
        self.master.title("Question")

        self.fram1 = Frame(self)
        self.fram1.pack(expand=YES, fill=BOTH)
        self.Label1 = Label(self.fram1, width=10, height=3, text=" " + self.in_data)
        self.Label1.pack(expand=YES, fill=BOTH)

        self.fram2 = Frame(self)
        self.fram2.pack(expand=YES, fill=BOTH)
        self.text1 = Text(self.fram2, name="text1", width=60, height=10)
        self.text1.pack(expand=YES, fill=BOTH, padx=5, pady=5)

        self.fram3 = Frame(self)
        self.fram3.pack(expand=YES, fill=BOTH)
        self.plainButton = Button(self.fram3, text="Exit", height=1, width=6, command=self.exitContent)
        self.plainButton.pack(side=RIGHT, padx=3, pady=3)

        self.plainButton1 = Button(self.fram3, text="Skip", height=1, width=6, command=self.skipContent)
        self.plainButton1.pack(side=RIGHT, padx=3, pady=3)

        self.plainButton2 = Button(self.fram3, text="Submit", height=1, width=6, command=self.submitContent)
        self.plainButton2.pack(side=RIGHT, padx=3, pady=3)
        self.flag = False

        self.chosen = IntVar()
        self.chosen.set(0)

        self.radioButton2 = Radiobutton(self.fram3, text="Overall score only",  variable=self.chosen, value = 0)
        self.radioButton2.pack(side=LEFT, padx=3, pady=3)

        self.radioButton1 = Radiobutton(self.fram3, text="Overall score with details", variable=self.chosen, value = 1)
        self.radioButton1.pack(side=LEFT, padx=3, pady=3)


    def requestQuestion(self,message):
        self.client.send(message.encode())
        self.recive()
        self.Label1.config(text=" " + str(self.in_data))


    def recive(self):
        self.in_data = self.client.recv(1024).decode()


    def dialog(self, title, message,score):
        respond = tkinter.messagebox.askquestion(title, message+score)
        if(respond == "yes"):
            self.skipContent()
        elif (respond == "no"):
            self.exitContent()


    def submitContent(self):
        message = self.text1.get(1.0, END)
        self.client.send(message.encode())
        self.recive()
        detailedScore = self.in_data
        message = "Overall"
        self.client.send(message.encode())
        self.recive()
        score = self.in_data
        print(detailedScore)
        print(self.in_data)
        self.score(detailedScore, score)


    def skipContent(self):
        self.text1.delete(1.0, END)
        self.requestQuestion("skip")


    def exitContent(self):
        self.text1.delete(1.0,END)
        message = "exit"
        self.client.send(message.encode())
        self.master.destroy()


    def score(self, detailedScore, score):
        score = score + "\nDo you want to continue?\n"
        if (self.chosen.get() == 0):
            self.dialog("Overall Score","", score)
        else:
            self.dialog("Overall Score with Details",detailedScore,score )





if __name__ == "__main__":
    SERVER = "127.0.0.1"
    PORT = 5003
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    completed = 1
    while completed:
        try:
            EntryDemo(client).mainloop()
        except ValueError:
            completed = 0
    client.close()










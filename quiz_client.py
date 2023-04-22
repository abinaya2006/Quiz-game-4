import socket
from threading import Thread
from tkinter import *


# nickname=input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))
print("Connected with the server...")


class GUI:

    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.label1 = Label(
            self.login, text="Please login to continue...", font="Helvetica 14 bold")
        self.label1.place(relheight=0.15, relx=0.2, rely=0)

        self.name = Label(self.login, text="Name: ", font="Helvetica 10",)
        self.name.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryName = Entry(self.login, font="Helvetic 12")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()

        self.go = Button(self.login, text="CONTINUE", font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rec = Thread(target=self.receive)
        rec.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_message(message)
            except:
                print("An error occured!")
                client.close()
                break

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")

        self.labelHead = Label(self.Window, bg="blue", fg="white", text=self.name, font="Helvetica 13 bold")
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window, width=450, bg="black")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textarea = Text(self.Window, width=20, height=2,
                             bg="#17202A", fg="#EAECEE", font="Helvetica 14")

        self.textarea.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
        
        self.labelBottom = Label(self.Window,bg="#ABB2B9",height=80)

        self.labelBottom.place(relwidth=1,rely=0.825)
        
        self.entryMsg = Entry(self.labelBottom,bg="#2C3E50",fg="#EAECEE",font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entryMsg.focus()

        self.sendMsg = Button(self.labelBottom,text="Send",font="Helvetica 10 bold",width=20,bg="#ABB2B9",command=lambda: self.sendButton(self.entryMsg.get()))

        self.sendMsg.place(relx=0.77,
                           rely=0.008,
                           relheight=0.06,
                           relwidth=0.22)

        self.textarea.config(cursor="arrow")

        scrollbar = Scrollbar(self.textarea)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textarea.yview)

        self.textarea.config(state = DISABLED)
        

    def sendButton(self, msg):
        self.textarea.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = Thread(target=self.write)
        snd.start()

    def show_message(self, message):
        self.textarea.config(state=NORMAL)
        self.textarea.insert(END, message+"\n\n")
        self.textarea.config(state=DISABLED)
        self.textarea.see(END)

    def write(self):
        self.textarea.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break


g = GUI()

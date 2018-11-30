from Tkinter import *
from random import randint
import thread
import time
file = open('al.txt', 'r')
bet = file.read().split()

def donothing():
   print offset.get()


def offint():
   try:
      num = int(offset.get())
      return num
   except:
      print "VOID"
      return "VOID"


def code():
   offset = offint()
   if(offset != "VOID"):
      message = msg.get("1.0",END)
   overall = len(message)
   thread.start_new_thread(coder,(offset,message,overall,))

def decode():
   offset = offint()
   if(offset != "VOID"):
      message = cmsg.get("1.0",END)
   overall = len(message)
   thread.start_new_thread(decoder,(offset,message,overall,))

   
def decoder(offset,message,overall):
   letters = []
   for letter in message:
      letters.append(letter)
   i = 0
   for l in letters:
      try:
         letterplace = bet.index(l)
         letterplace = letterplace - offset
         while(letterplace < 0):
            letterplace = letterplace + len(bet) 
         l = bet[letterplace]
      except:
         l = " "
      msg.insert(INSERT,l)
      i = i + 1
      text = "Progress %s/%s"% (i, overall)
      v.set(text)
   cmsg.delete("1.0",END)
def coder(offset,message,overall):
   letters = []
   for letter in message:
      letters.append(letter)
   i = 0
   for l in letters:
      try:
         letterplace = bet.index(l)
         letterplace = letterplace + offset
         while(letterplace > len(bet)):
            letterplace = letterplace - len(bet)
         l = bet[letterplace]
      except:
         l = " "
      cmsg.insert(INSERT, l)
      i = i + 1
      text = "Progress %s/%s"% (i, overall)
      v.set(text)
   msg.delete("1.0",END)

def generate():
    offset.delete(0,END)
    offset.insert(0,randint(1,1000))


def save():
   date = time.strftime("%d/%m/%Y %H:%M:%S")
   try:
      #Each line means a new var. Hopefully no one will manually edit it as it won't work!
      f = open(date + ".sav","w") #opens file with name of "location"
      f.write(off.get() + "\n")

      #as the letters aren't always ascii, we'll convert them to numbers
      t = ""
      for letter in msg.get("1.0",END):
         letter = ord(letter) #convert to number
         t = t + "%s-"% letter #joins each letter together (as a number) but splits numbers with a "-"

         f.write(t + "\n")
         t = ""
      for letter in cmsg.get("1.0",END):
         letter = ord(letter) #convert to number
         t = t + "%s-"% letter#joins each letter together (as a number) but splits numbers with a "-"
         f.write(t + "\n")#writes to file (location)


      f.close()
      v.set("SAVED")
   except:
      v.set("ERROR, COULD NOT SAVE")

def clear():
   offset.delete(0,END)
   msg.delete("1.0",END)
   cmsg.delete("1.0",END)
def ui():
    root = Tk()
    root.title("~My Program~")
    #menu
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Clear", command=clear)
    filemenu.add_command(label="Save", command=save)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Random test", command=donothing)
    menubar.add_cascade(label="System", menu=filemenu)
    root.config(menu=menubar)

    #offset input & gen
    global offset
    Label(root,text="Offset(1 to 1000): ",fg="red").grid(row=1,column=1)
    offset = Spinbox(root, from_=0, to=1000)
    offset.grid(row=1,column=2)
    Button(root,text="Generate",command=generate).grid(row=1,column=3)

    #input the message
    global msg
    Label(root,text="Orginal message",fg="red").grid(row=2,column=1)
    msg = Text(root,width=45,height=5)
    msg.grid(row=3,column=1,columnspan=3)
    Button(root,text="Code message",command=code).grid(row=4,column=3)

    #input the coded message
    global cmsg
    Label(root,text="Coded message",fg="red").grid(row=5,column=1)
    cmsg = Text(root,width=45,height=5)
    cmsg.grid(row=6,column=1,columnspan=3)
    Button(root,text="Decode message",command=decode).grid(row=8,column=3)

   #progress
    global v
    v = StringVar()
    Label(root,text="Progress 0/0",fg="blue",textvariable=v).grid(row=9,column=1)
    
    #start
    root.mainloop()
ui()

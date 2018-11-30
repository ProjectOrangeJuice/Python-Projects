#Imports
from Tkinter import *
import tkMessageBox
root = Tk()


alphale = ["a","b","c","d","e","f","g","h","i","j","k","l", "m", "n" ," ", "o", "p", "q", "r", "s", "t" , "u" , "v" , "w" , "x" , "y" , "z", "A","B","C","D","E","F","G","H","I","J","K","L", "M", "N" , "O", "P", "Q", "R", "S", "T" , "U" , "V" , "W" , "X" , "Y" , "Z"  "none" ]


def test():
    e= False #if this is true, it means there is an error - stops running the rest.
    #This tests the vaules
    if(option.get() == 0): #Options are 1 or 2. 1 being code and 2 being decode
        tkMessageBox.showinfo("Error", "Select an option.")
        e=True
    print off.get()#helps me debug my program

    try: #if ANY error comes up, it will go straight to except
        if(int(off.get()) < -25 or int(off.get()) > 25): #validates number
            tkMessageBox.showinfo("Error", "Offset must be between -25 to 25")
            e=True
    except:
        tkMessageBox.showinfo("Error", "Offset must be a whole number")
        e=True
    #print msg.get("1.0",END)
    #print cmsg.get("1.0",END)
    if not e:
        try:
            if(option.get()==1):
                code()
            if(option.get()==2):
                decode()
        except:
            tkMessageBox.showinfo("Error", "Please enter text into the message box")#this is a possible error in my program

def opengui():
    popup= Tk()
    root.title("Open")#window name
    Label(popup, text="File name:").grid(row=1,column=1, sticky=W)#text display
    e = Entry(popup)
    e.grid(row=1,column=2)
    Button(popup,text="Open",command=lambda: opener(e.get())).grid(row=6,column=1)#when clicked it will run another function
    popup.mainloop() 


def saver(location):#(location) asks for a var when running function
    try:
        #Each line means a new var. Hopefully no one will manually edit it as it won't work!
        f = open(location + ".sav","w") #opens file with name of "location"
        f.write(off.get() + "\n")

        #as the letters arent always ascii, we'll convert them to numbers
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
        tkMessageBox.showinfo("Saved!", "to open the file, press 'open' and type '%s'"% location)

    except:#any errors -> will run this function
         tkMessageBox.showinfo("Error", "Enter a file name")


def opener(location):
  
    f = open(location + ".sav", "r")#open the file READ ONLY

    i = 0
    while i <3:#there SHOULD only be 3 lines, so we'll only going to read 3 lines.
        line = f.next().strip()
        #print line

        if(i ==0):#line 1
            off.set(line)#sets the gui element (offset) to what ever the value is.
                
        if(i == 1):#line 2
           l = line.split("-")#this will create an array which  i joined together with "-"
           msg.delete("1.0",END)
           for le in l:
                if(le == ""):break#if blank
                eletter = chr(int(le))#converr number to letter
                msg.insert(INSERT, eletter)

        if(i == 2):
           l = line.split("-")#this will create an array which  i joined together with "-"
           cmsg.delete("1.0",END)
           for le in l:
                if(le == ""):break
                eletter = chr(int(le))#convert letter to number
                cmsg.insert(INSERT, eletter)
        i = i + 1
    f.close()#close the file


def save():
    popup= Tk()
    root.title("Save")#sets the window name
    Label(popup, text="File name:").grid(row=1,column=1, sticky=W)#creates a lable (text)
    e = Entry(popup)#user input
    e.grid(row=1,column=2)#add to screen
    Button(popup,text="Save",command=lambda: saver(e.get())).grid(row=6,column=1)#when the button is clicked it runs a function
    popup.mainloop()  #begins loop

def code():
 
    #Now, we want to split each character of the message
    letters = []
    amount = 0
    for letter in msg.get("1.0",END):#gets input from the very start (row one, column one)
        letters.append(letter)#adds to list
        amount = amount + 1
    runs = 0
    print amount
    run = True
    nmsg =""#join the list together
    #now the letters are apart, time to turn them into numbers + the offset
    for l in letters:#each value in letter
        run = True
        if(runs == amount-1 ):
            break
        print "********CODE*********"
        print "orginal letter: ",l 
        i = 0
        num = 0
        for le in alphale:
            
            if(le == l):
                print "letter found, number: ",i
                num = i
                break
            if(le == "none"):
                nmsg = nmsg + l
                run = False
                break
            i = i + 1
        num = num + int(off.get())#adds the offset to the orginal number, it has to be converted to int or it will think its a letter.
        while(num > 51):
            num = num - 26
        print "number: ",num
        print alphale[num]
        if(run):
            nmsg = nmsg + alphale[num]
            runs = runs + 1

    print nmsg
    cmsg.delete("1.0",END)#deletes anything in the input
    msg.delete("1.0",END)#deletes anything in the input
    cmsg.insert(INSERT, nmsg)#adds to the input screen

def decode():
   
    #Now, we want to split each character of the message
    letters = []
    amount = 0
    for letter in cmsg.get("1.0",END):#gets input from the very start (row one, column one)
        letters.append(letter)#adds to list
        amount = amount + 1
    runs = 0
    run = True
    nmsg =""#join the list together
    #now the letters are apart, time to turn them into numbers + the offset
    for l in letters:#each value in letter
        if(runs == amount-1):
            break
        print "********DECODE*********"
        print "orginal letter: ",l 
        i = 0
        num = 0
        for le in alphale:

            if(le == l):
                print "letter found, number: ",i
                num = i
                break
            if(le == "none"):
                nmsg = nmsg + l# add the letter to the variable
                run = False
                break
            i = i + 1
        num = num - int(off.get())
        while(num > 50):
            num = num - 26
        print "number: ",num
        print alphale[num]
        if(run):
            nmsg = nmsg + alphale[num]
            runs = runs + 1

    print nmsg
    msg.delete("1.0",END)#deletes anything in the input
    msg.insert(INSERT, nmsg)#adds to the input screen


    
#vars
off = StringVar()#these will be used as the user inputs (means i can get the values from any function)
option = IntVar()

#gui

root.title("Code/Decode")

#option, to code the message or decode it.
Radiobutton(root, text="code",variable=option, value=1).grid(row=1,column=1,sticky=W)#radio button - code OR decode
Radiobutton(root, text="decode",variable=option, value=2).grid(row=1,column=1)

#lables so the user knows what it is
Label(root, text="Offset:").grid(row=2,column=1, sticky=W)
Label(root, text="Message").grid(row=3,column=1, sticky=W)
Label(root, text="Coded Message").grid(row=5,column=1, sticky=W)



#inputs
Entry(root, textvar=off).grid(row=2,column=1, columnspan=2, sticky=W, padx=50)
msg = Text(root,width=50,height=10)
msg.grid(row=4,column=1)
cmsg = Text(root,width=50,height=10)
cmsg.grid(row=6,column=1)


#finally run the program
Button(root,text="Run",command=test).grid(row=7,column=1,sticky="W")
#save and open
Button(root,text="Save", command=save).grid(row=7,column=1,sticky="E")
Button(root,text="Open", command=opengui).grid(row=7,column=1,sticky="N")
root.mainloop()  


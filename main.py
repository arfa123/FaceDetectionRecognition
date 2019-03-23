from guizero import App, PushButton, Box, Text, Window, TextBox, ListBox
from gpiozero import Button
from faceDetectionTest import testCamera
from faceDetection import faceDetection
from faceTrainer import faceTrainer
from faceRecognizer import faceRecognizer
import sqlite3 as lite
import os
import shutil

def showMainWin():
    entryWinTitleBox.hide()
    recogWinTitleBox.hide()
    entryForm.hide()
    addBtnBox.hide()
    usersListBox.hide()
    titleBox.show()
    userEntryBtn.show()
    faceRecogBtn.show()

def showUserEntryWin():
    titleBox.hide()
    recogWinTitleBox.hide()
    userEntryBtn.hide()
    faceRecogBtn.hide()
    entryWinTitleBox.show()
    entryForm.show()
    addBtnBox.show()
    usersListBox.show()

def showRecogWin():
    faceRecognizer()

def showTestCamera():
    name = userName.value.capitalize()
    Id = userId.value
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id INT, name TEXT)")
        cur.execute("SELECT * FROM users WHERE id=:ID", {"ID": Id})
        row = cur.fetchone()
        con.commit()
        if len(name) > 3 and name.isalpha() and Id.isnumeric() and row == None:
            val = testCamera(faceDetection, userName.value, userId.value, faceTrainer)
            if type(val) is str and len(val) > 4:
                users.append(val)
                usersList.append(val)

def deleteSelectedUser():
    print("Delete that user:",usersList.value, users)
    if usersList.value in users:
        userIdName = usersList.value.split(". ")
        print("userIdName:",type(userIdName), userIdName[0], userIdName[1])
        cur.execute("DELETE FROM users WHERE id=:ID", {"ID": userIdName[0]})
        con.commit()
        users.remove(usersList.value)
        usersList.remove(usersList.value)
        if(os.path.isdir("dataset/"+userIdName[1]+"."+userIdName[0])):
                shutil.rmtree("dataset/"+userIdName[1]+"."+userIdName[0])
                faceTrainer()

################# Connect to Database #####################
con = lite.connect("users.db")
users = []
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INT, name TEXT)")
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    con.commit()
    for i in range(0, len(users)):
        users[i] = ". ".join(str(x) for x in users[i])

################# Main Window Elements #####################
app = App(title="Face Detection and Recognization", width="800")
titleBox = Box(app, width="fill", align="top")
pageTitle = Text(titleBox, text="Welcome to Face Detection and Recognization Project", color="blue", size=20)
userEntryBtn = PushButton(app, command=showUserEntryWin, text="Add New User")
userEntryBtn.bg = "red"
userEntryBtn.text_size = 15
userEntryBtn.text_color = "#ffffff"
faceRecogBtn = PushButton(app, command=showRecogWin, text="Recognize User")
faceRecogBtn.bg = "green"
faceRecogBtn.text_size = 15
faceRecogBtn.text_color = "#ffffff"

################### Add User Window Elements ###############
entryWinTitleBox = Box(app, layout="grid", width="fill", align="top")
addWinBackButton = PushButton(entryWinTitleBox, text="Go back", grid=[0,0], command=showMainWin)
entryPgTitle = Text(entryWinTitleBox, text="Add New User", color="blue", size=20, grid=[1,0])
entryForm = Box(app, width="fill", layout="grid")
nameLabel = Text(entryForm, text="Enter User Name", grid=[0,0], align="left")
userName = TextBox(entryForm, text="", grid=[1,0], width="fill")
idLabel = Text(entryForm, text="Enter User Id", grid=[0,1], align="left")
userId = TextBox(entryForm, text="", grid=[1,1], width="fill")
addBtnBox = Box(app, width="fill")
addButton = PushButton(addBtnBox, text="Add User", command=showTestCamera)
usersListBox = Box(app)
usersList = ListBox(usersListBox, width="fill", items=users, scrollbar=True)
deleteUserBtn = PushButton(usersListBox, text="Delete User", command=deleteSelectedUser)

################# Recognize User Window Elements ##########
recogWinTitleBox = Box(app, layout="grid", width="fill", align="top")
recogWinBackButton = PushButton(recogWinTitleBox, text="Go back", grid=[0,0], command=showMainWin)
recogPgTitle = Text(recogWinTitleBox, text="Recognize User", color="blue", size=20, grid=[1,0])

showMainWin()

runFaceRecogBtn = Button(2)
runFaceRecogBtn.when_pressed = showRecogWin

app.display()
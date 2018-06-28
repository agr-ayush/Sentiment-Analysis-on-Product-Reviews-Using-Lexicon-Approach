import sqlite3
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
from tkinter import *

a = ""
list1 = []
rev = []

features = ["CAMERA", "CHARGER", "DISPLAY", "BATTERY", "PROCESSOR", "RAM", "SPEAKER", "TOUCH", "SCREEN", "BUTTONS",
            "SIM CARD"]
positive = 0
negative = 0
neutral = 0
positive1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
negative1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class Application:
    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        self.listcreation()
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, state='readonly', width=75)
        self.box.bind("<<ComboboxSelected>>", self.choosePhone)
        self.box['values'] = list1
        self.box.current(0)
        self.box.grid(column=0, row=1, columnspan=4, padx=10, pady=10)

    def listcreation(self):
        with open('E:\data.csv', encoding="utf8") as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            rows = [r[0] for r in readCSV]
            temp = rows[0]
            if rows[0]:
                for row in rows:
                    if row not in temp:
                        list1.append(row)
                        temp = row

    def choosePhone(self, item):
        conn = sqlite3.connect('E:\Phone_Info.db')
        global cur
        cur = conn.cursor()
        cur.execute('SELECT * FROM Database WHERE Phone_Name = ? ', (self.box.get(),))
        rows = (cur.fetchall())
        global details
        details = []
        for row in rows:
            for x in row:
                details.append(x)
        global negative_data
        global positive_data
        negative_data = []
        positive_data = []
        negative_data.extend((details[4], details[6], details[8], details[10], details[12], details[14], details[16],
                              details[18], details[20], details[22], details[24]))
        positive_data.extend((details[3], details[5], details[7], details[9], details[11], details[13], details[15],
                              details[17], details[19], details[21], details[23]))

def showDetails():
    plt.close()
    labels = ["Positive", "Negative"]
    values = [details[1], details[2]]
    explode = [.1, .1]
    plt.title('Overall')
    plt.pie(values, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%')
    plt.legend()
    plt.axis('equal')
    plt.show()


def showProsandCons():
    root3 = Tk()
    a =""
    b=""
    for i, j, k in zip(positive_data, negative_data, features):
        if (i != 0 and j != 0) or (i == 0) and (j != 0) or (j == 0 and i != 0):
            if i > abs(j):
                a = a + k + "\n"
            else:
                b = b + k + "\n"

    if b == "CONS  \n\n":
        b = ""
    if a == "PROS  \n\n":
        a = ""
    label7 = Label(root3, text="PROS", font=('bold', 25))
    label8 = Label(root3, text="CONS", font=('bold', 25))
    label5= Label(root3, text=a+"\n\n===========================", font=(10))
    label6 = Label(root3, text=b, font=(10))
    label7.grid(row=0)
    label5.grid(row=1)
    label8.grid(row=2)
    label6.grid(row=3)
    root3.minsize(100, 200)

    root3.mainloop()


def showfeaturedetail():
    plt.close()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for a in range(0, 10):
        values[a] = positive_data[a] + abs(negative_data[a])
    toprint1 = ['', '', '', '', '', '', '', '', '', '']
    for b in range(0, 10):
        toprint1[b] = str(positive_data[b]) + "/" + str(values[b])
    toprint2 = ['', '', '', '', '', '', '', '', '', '']
    for b in range(0, 10):
        toprint2[b] = str(abs(negative_data[b])) + "/" + str(values[b])
    plt.figure(figsize=(20, 10))
    ax = plt.subplot()
    ax.set_title('Features')
    ax.set_xlabel("List of Features")
    ax.set_ylabel("Number of Reviews")
    ax.bar(x, negative_data, width=1, color='r', edgecolor='0', label='Negative Review')
    ax.bar(x, positive_data, width=1, color='g', edgecolor='0', label='Positive Review')
    ax.legend()
    rects = ax.patches
    h = plt.Axes.get_ylim(ax)
    labels = features
    for rect, label, r in zip(rects, labels, range(0, 10)):
        ax.text(rect.get_x() + rect.get_width() / 2, 0, label, ha='center', va='bottom')
        ax.text(rect.get_x() + rect.get_width() / 2, h[1]/2, toprint1[r], ha='center', va='bottom')
        ax.text(rect.get_x() + rect.get_width() / 2, h[0]/2, toprint2[r], ha='center', va='bottom')
    plt.show()

def displayfeatures():
    root1 = Tk()
    label = Label(root1,text="Enter a Feature:",font=('bold'))
    label.grid(row=0)
    global textfield
    textfield = Entry(root1)
    textfield.grid(row=1)
    button5 = Button(root1, text="Features", font=('bold'), padx=10, pady=10, command=bestphone)
    button5.grid(row=2)
    global label2
    label2 = Label(root1, text="", font=('bold'))
    label2.grid(row=3)
    root1.minsize(200,150)

    root1.mainloop()

def bestphone():
   # print("The best Phone is")
    feature = textfield.get()
    #print(feature)
    if feature.upper().__eq__("CAMERA"):
        cur.execute("SELECT Camera_Positive FROM Database")
    elif feature.upper().__eq__("CHARGER"):
        cur.execute("SELECT Charger_Positive FROM Database")
    elif feature.upper().__eq__("DISPLAY"):
        cur.execute("SELECT Display_Positive FROM Database")
    elif feature.upper().__eq__("BATTERY"):
        cur.execute("SELECT Battery_Positive FROM Database")
    elif feature.upper().__eq__("PROCESSOR"):
        cur.execute("SELECT Processor_Positive FROM Database")
    elif feature.upper().__eq__("RAM"):
        cur.execute("SELECT RAM_Positive FROM Database")
    elif feature.upper().__eq__("SPEAKER"):
        cur.execute("SELECT Speaker_Positive FROM Database")
    elif feature.upper().__eq__("TOUCH"):
        cur.execute("SELECT Touch_Positive FROM Database")
    elif feature.upper().__eq__("SCREEN"):
        cur.execute("SELECT Screen_Positive FROM Database")
    elif feature.upper().__eq__("BUTTONS"):
        cur.execute("SELECT Button_Positive FROM Database")
    elif feature.upper().__eq__("SIMCARD"):
        cur.execute("SELECT SIM_Card_Positive FROM Database")

    result_set = cur.fetchall()
    list = []
    for row in result_set:
        for x in row:
            list.append(x)
    list2 = []
    for x in list:
        list2.append(x)
   # print(list)
    cur.execute("SELECT Phone_Name FROM Database")
    result_set1 = cur.fetchall()
    list1 = []
    for row in result_set1:
        for x in row:
            list1.append(x)
    i = 0
    list.sort()
    #print(list)
    b = list[-1]
    c = list[-2]
    d = list[-3]
    string = ''
    #print(list2)
    for a in list2:
        if a is b:
            string1 = "First Suggestion: " + list1[i] + "\n"
        if a is c:
            string2 = "Second Suggestion: " + list1[i] + "\n"
        if a is d:
            string3 = "Third Suggestion: " + list1[i] + "\n"
        i = i + 1
    string = string1 + string2 + string3
    label2.config(text = string)


if __name__ == '__main__':
    root = Tk()
    label = Label(root, text="Sentiment Analysis and Polarity Check", font=('bold', 20), )
    label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
    app = Application(root)
    button1 = Button(root, text="Show Overall", font=('bold'), padx=10, pady=10, command=showDetails)
    button1.grid(row=2, column=0)
    button2 = Button(root, text="Show Features", font=('bold'), padx=10, pady=10, command=showfeaturedetail)
    button2.grid(row=2, column=1)
    button3 = Button(root, text="Pros and Cons", font=('bold'), padx=10, pady=10, command=showProsandCons)
    button3.grid(row=2, column=2)
    button4 = Button(root, text="Features", font=('bold'), padx=10, pady=10, command=displayfeatures)
    button4.grid(row=2, column=3)
    root.minsize(600, 250)

    root.mainloop()
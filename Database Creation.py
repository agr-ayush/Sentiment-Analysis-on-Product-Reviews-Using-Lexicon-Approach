from tkinter import ttk
import csv
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords
from tkinter import *
import sqlite3

list1 = []
features = ["CAMERA", "CHARGER", "DISPLAY", "BATTERY", "PROCESSOR", "RAM", "SPEAKER", "TOUCH", "SCREEN", "BUTTONS",
            "SIM CARD"]


class DatabaseCreation:
    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def combo(self):
        global conn
        conn = sqlite3.connect('Phone_Info.db')
        global cur
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS Database')
        cur.execute(
            'CREATE TABLE Database (Phone_Name TEXT, Positive_Reviews INTEGER, Negative_Reviews INTEGER, Camera_Positive INTEGER, Camera_Negative INTEGER,Charger_Positive INTEGER, Charger_Negative INTEGER,Display_Positive INTEGER, Display_Negative INTEGER, Battery_Positive INTEGER, Battery_Negative INTEGER,Processor_Positive INTEGER, Processor_Negative INTEGER,RAM_Positive INTEGER, RAM_Negative INTEGER,Speaker_Positive INTEGER, Speaker_Negative INTEGER,Touch_Positive INTEGER, Touch_Negative INTEGER,Screen_Positive INTEGER, Screen_Negative INTEGER,Button_Positive INTEGER, Button_Negative INTEGER,SIM_Card_Positive INTEGER, SIM_Card_Negative INTEGER)')

        #conn.close()
        self.listcreation()
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value, state='readonly', width=75)
        self.box.bind("<<ComboboxSelected>>")
        self.box['values'] = list1
        self.box.current(0)
        self.box.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

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
        print(list1)
        for Phone in list1:
            global positive1
            positive1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            global negative1
            negative1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


            with open('E:\data.csv', encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                count = 0
                flag = 1
                index1 = 0
                index2 = 0
                count_positive = 0
                count_negative = 0
                count_neutral = 0
                for row in reader:
                    count += 1
                    if Phone in row[0]:
                        if flag == 1:
                            index1 = count
                            flag = 0
                        else:
                            index2 = count
                count = 0
                csvfile.seek(0)
                for row1 in reader:
                    count += 1
                    if count in range(index1 + 1, index2 + 1):
                        stop_words = set(stopwords.words('english'))
                        self.featuretext(row1[4])
                        sentences = nltk.sent_tokenize(row1[4])
                        sentences1 = [a.upper() for a in sentences]
                        stokens = [nltk.word_tokenize(sent) for sent in sentences1]
                        taggedlist = []
                        for stoken in stokens:
                            for w in stoken:
                                if w in stop_words:
                                    stoken.remove(w)
                            taggedlist.append(nltk.pos_tag(stoken))
                        wnl = nltk.WordNetLemmatizer()

                        score_list = []
                        for idx, taggedsent in enumerate(taggedlist):
                            score_list.append([])
                            for idx2, t in enumerate(taggedsent):
                                lemmatized = wnl.lemmatize(t[0])
                                if t[1].startswith('NN'):
                                    newtag = 'n'
                                elif t[1].startswith('JJ'):
                                    newtag = 'a'
                                elif t[1].startswith('V'):
                                    newtag = 'v'
                                elif t[1].startswith('R'):
                                    newtag = 'r'
                                else:
                                    newtag = ''
                                if newtag != '':
                                    synsets = list(swn.senti_synsets(lemmatized, newtag))
                                    score = 0
                                    if len(synsets) > 0:
                                        for syn in synsets:
                                            score += syn.pos_score() - syn.neg_score()
                                        score_list[idx].append(score / len(synsets))
                        sentence_sentiment = []

                        for score_sent in score_list:
                            if len(score_sent) != 0:
                                sentence_sentiment.append(
                                    sum([word_score for word_score in score_sent]) / len(score_sent))
                        score = 0
                        for i in sentence_sentiment:
                            score += i
                        if score > 0:
                            count_positive = count_positive + 1

                        if score < 0:
                            count_negative = count_negative + 1

                        if score == 0:
                            count_neutral = count_neutral + 1

                global negative
                global positive
                global neutral
                negative = count_negative
                positive = count_positive
                neutral = count_neutral
                print("Negative Count = " + str(count_negative))
                print("Positive Count = " + str(count_positive))
                print("Neutral Count = " + str(count_neutral))
                print(positive1)
                print(negative1)
                cur.execute("INSERT INTO Database VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (Phone, positive, negative,positive1[0],negative1[0],positive1[1],negative1[1],positive1[2],negative1[2],positive1[3],negative1[3],positive1[4],negative1[4],positive1[5],negative1[5],positive1[6],negative1[6],positive1[7],negative1[7],positive1[8],negative1[8],positive1[9],negative1[9],positive1[10],negative1[10]))
                conn.commit()
        conn.close()

    def featuretext(self, review):
        sentences = nltk.sent_tokenize(review)
        sentences1 = [a.upper() for a in sentences]
        stokens = [nltk.word_tokenize(sent) for sent in sentences1]

        taggedlist = []
        stop_words = set(stopwords.words('english'))
        for stoken in stokens:
            for w in stoken:
                if w in stop_words:
                    if w != 'but' or w != 'and':
                        stoken.remove(w)
            taggedlist.append(nltk.pos_tag(stoken))
        list1 = []
        for idx, taggedsent in enumerate(taggedlist):
            for idx2, t in enumerate(taggedsent):
                flag = 1
                flag2 = 1
                for a in features:
                    if t[0] == a:
                        list1.append(a)
                    if t[0] == 'but' and flag2 == 1:
                        list1.append('but')
                        flag2 = 0
                    if t[1].startswith('JJ') and flag == 1:
                        list1.append(t[0])
                        flag = 0
        count = 0
        for a in features:
            if list1.__contains__(a):
                score_list = []
                for idx, taggedsent in enumerate(taggedlist):
                    score_list.append([])
                    for idx2, t in enumerate(taggedsent):
                        wnl = nltk.WordNetLemmatizer()
                        lemmatized = wnl.lemmatize(t[0])
                        if t[1].startswith('NN'):
                            newtag = 'n'
                        elif t[1].startswith('JJ'):
                            newtag = 'a'
                        elif t[1].startswith('V'):
                            newtag = 'v'
                        elif t[1].startswith('R'):
                            newtag = 'r'
                        else:
                            newtag = ''
                        if newtag != '':
                            synsets = list(swn.senti_synsets(lemmatized, newtag))
                            score = 0
                            if len(synsets) > 0:
                                for syn in synsets:
                                    score += syn.pos_score() - syn.neg_score()
                                score_list[idx].append(score / len(synsets))
                sentence_sentiment = []
                for score_sent in score_list:
                    if len(score_sent) != 0:
                        sentence_sentiment.append(sum([word_score for word_score in score_sent]) / len(score_sent))
                score = 0
                for i in sentence_sentiment:
                    score += i
                if score > 0:
                    positive1[count] = positive1[count] + 1
                if score < 0:
                    negative1[count] = negative1[count] - 1
            count = count + 1


if __name__ == '__main__':
    root = Tk()
    app = DatabaseCreation(root)
    root.mainloop()
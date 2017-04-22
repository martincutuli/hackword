# -*- coding: utf_8 -*-
import pandas as pd
import sqlite3,argparse,enchant

#HackWord 0.2beta
# by @a_l_e_p_h
# Create dictionary for bruteforce using leets dictionary and top of passwords hacked

def permutation(word):
    d = enchant.Dict("en_US")
    return d.suggest(word)

def leet(connection,word):
    query = "select * from leet"
    cursor = connection.cursor()
    cursor.execute(query)
    leetsbd = cursor.fetchall()
    letters = list(word)
    wordsreturn = []
    wordsreturn.append(word)
    for leetword in leetsbd:
        word = word.replace(leetword[0],leetword[1])
    wordsreturn.append(word)

    return wordsreturn

df = pd.DataFrame()
connection = sqlite3.connect('words.db')
query="select word,frecuency,length(word) as len from hackword order by frecuency desc"
dfWord = pd.read_sql_query(query,connection)

parser = argparse.ArgumentParser(prog='HackWord', usage='%(prog)s [w][m][M][0]')
parser.add_argument('-w', '--word',
                    required=True, type=int, help='number of words of dict')
parser.add_argument('-m', '--min',
                    required=True, type=int, help='Min letter')
parser.add_argument('-M', '--max',
                    required=False, type=int, help='Max letter')
parser.add_argument('-s', '--scrambled',
                    required=False, type=str, help='scrambled words')

args = parser.parse_args()

if args.max:
    dfRead = dfWord.loc[(dfWord["len"] > args.min ) & (dfWord["len"] <= args.max)]
else:
    dfRead = dfWord.loc[dfWord["len"] > args.min]

if args.scrambled:
    if args.scrambled == "normal":
        scrambled = "normal"
    elif args.scrambled == "leet":
        scrambled = "leet"
    elif args.scrambled == "both":
        scrambled = "both"
    else:
        print("Options of scrambled are normal | leet | both")
        exit()
dfRead = dfRead[0:args.word]

dictword = []
print("Running process to create HackWord")
for index, row in dfRead.iterrows():
    if args.scrambled:
        if row["word"].isdigit():
            dictword.append(row["word"])
        else:
            if scrambled == "normal":
                suggestions = permutation(str(row["word"]))
                for suggestion in suggestions:
                    if len(suggestion) > args.min:
                        dictword.append(suggestion)
            elif scrambled == "leet":
                leets = leet(connection,str(row["word"]))
                for leetswords in leets:
                    dictword.append(leetswords)
            elif scrambled == "both":
                suggestions = permutation(str(row["word"]))
                for suggestion in suggestions:
                    leets = leet(connection,suggestion)
                    for leetswords in leets:
                        dictword.append(leetswords)
    else:
        dictword.append(row["word"])

fi = open("HackWord.txt","w")
for word in dictword:
    fi.write(word + "\n")
fi.close()
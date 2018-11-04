#!/usr/bin/python
import list_of_games
import os
import requests
import bs4
import sqlite3 as lite
import sys
import time

nin_games = """
Laser - 1973
EVR Race - 1975
Wild Gunman - 1976
Donkey Kong - 1983
Donkey Kong Jr. - 1983
Popeye - 1983
Mahjong - 1983
Gomoku Narabe Renju - 1983
Mario Bros. - 1983
Popeye no Eigo Asobi - 1983
Baseball - 1984
Donkey Kong Jr. Math - 1984
Tennis - 1984
Pinball - 1984
Wild Gunman - 1984
Duck Hunt - 1984
Golf - 1984
Hogan's Alley - 1984
Family BASIC - 1984
Donkey Kong 3 - 1984
Devil World - 1984
Clu Clu Land - 1984
4-Nin Uchi Mahjong - 1984
Excitebike - 1984
F-1 Race - 1984
Urban Champion - 1984
Ice Climber - 1984
Donkey Kong Jr. + Jr. Sansū Lesson - 1984
Balloon Fight - 1985
Family BASIC V3 - 1985
Kung Fu - 1985
Wrecking Crew - 1985
Stack-Up - 1985
Gyromite - 1985
10-Yard Fight - 1985
Super Mario Bros. - 1985
Soccer - 1985
Mach Rider - 1985
Gumshoe - 1986
Volleyball - 1987
Pro Wrestling - 1987
Metroid - 1987
Kid Icarus - 1987
The Legend of Zelda - 1987
Slalom - 1987
Stadium Events - 1987
Mike Tyson's Punch-Out!! - 1987
Rad Racer - 1987
Ginga no Sannin - 1987
R.C. Pro-Am - 1988
Ice Hockey - 1988
Famicom Wars - 1988
Donkey Kong Classics - 1988
Super Mario Bros. 2 - 1988
Anticipation - 1988
Super Mario Bros. + Duck Hunt - 1988
Super Team Games - 1988
Zelda II: The Adventure of Link - 1988
Dance Aerobics - 1989
Cobra Triangle - 1989
Dragon Warrior - 1989
Faxanadu - 1989
Mother - 1989
Tetris - 1989
To the Earth - 1989
Short Order & Eggsplode - 1989
Super Mario Bros. 3 - 1990
Super Spike V'Ball - 1990
Pin*Bot - 1990
Final Fantasy - 1990
Snake Rattle 'n Roll - 1990
Barker Bill's Trick Shooting - 1990
NES Play Action Football - 1990
Dr. Mario - 1990
Fire Emblem: Shadow Dragon and the Blade of Light - 1990
Nintendo World Cup - 1990
StarTropics - 1990
Stealth A.T.F. - 1990
Super Mario Bros. + Duck Hunt + World Class Track Meet - 1990
Super Spike V'Ball + Nintendo World Cup - 1990
The Battle of Olympus - 1991
NES Open Tournament Golf - 1991
Shin 4 Nin Uchi Mahjong: Yakuman Tengoku - 1991
Solstice: The Quest for the Staff of Demnos - 1991
Super Mario Bros. + Tetris + Nintendo World Cup - 1991
Battletoads & Double Dragon - 1992
Fire Emblem Gaiden - 1992
Mega Man 3 - 1992
The Guardian Legend - 1992
Yoshi - 1992
Yoshi's Cookie - 1993
Joy Mech Fight - 1993
Kirby's Adventure - 1993
Mario Bros. Classic Series - 1993
Mega Man 4 - 1993
Mega Man 5 - 1993
    """
## dd/mm/yyyy format
# print (time.strftime("%d/%m/%Y"))
# print ("HI " + time.strftime("%d"))
# print (time.strftime("%m"))
# print (time.strftime("%Y"))

def howToPrintDataFromTable(db, table):
    pass

def createConnection(db_file):
    """ create a database connection to a SQLite database """
    # when you make a connection to an unexisting db, sqlite creates that db!
    try:
        conn = lite.connect(db_file)
    except Error as e:
        print(e)
    finally:
        conn.close()

def createTable(db, table_name):
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        sqlite_command_drop = "DROP TABLE IF EXISTS "+ table_name
        sqlite_command_create = "CREATE TABLE "+ table_name +"(nome_jogo VARCHAR(200), ano_criado INT)"
        cur.execute(sqlite_command_drop)
        cur.execute(sqlite_command_create)
        print("Table " + table_name + " was created.")
    if con:
        con.close()

def printAllTablesOfDb(db):
    con = lite.connect(db)
    # SELECT
    with con:
        cur = con.cursor()
        # From within a C/C++ program (or a script using Tcl/Ruby/Perl/Python bindings) you can get access to table and index names by doing a SELECT on a special table named "SQLITE_MASTER". Every SQLite database has an SQLITE_MASTER table that defines the schema for the database. ... The SQLITE_MASTER table is read-only.
        # select todas tables da db. sqlite_master é uma table especial que toda db tem, ela é read-only
        res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res:
            print (name[0])
    if con:
        con.close()

# INSERT
# argument is one list with the 7 values we need for the company data
def insertIntoTable(db, list_with_data, table_name):
    connection_to_db = lite.connect(db)
    with connection_to_db: 
        cur = connection_to_db.cursor()
        sqlite_command_insert = "INSERT INTO " + table_name + " VALUES (?, ?)"
        cur.execute(sqlite_command_insert, list_with_data)
    if connection_to_db:
        connection_to_db.close()

# SELECT
def selectFromTable(db, table_name):
    connection_to_db = lite.connect(db)
    with connection_to_db: 
        cur = connection_to_db.cursor()
        # cur.execute("SELECT nome_jogo, ano_criado FROM " + table_name)
        # cur.execute("SELECT * FROM " + table_name)
        # cur.execute("SELECT * FROM " + table_name + " WHERE nome_jogo='Donkey Kong'")
        cur.execute("SELECT * FROM " + table_name + " ORDER BY nome_jogo ASC")

        # obs: fetchone pega o 1º resultado e remove ele da "array". por isso que se rodar dois fetchone seguidos o segundo retorna none.
        # data = cur.fetchone()
        # print (data)
        # print ("\n")
        data = cur.fetchall()
        print (data)
    if connection_to_db:
        connection_to_db.close()

# helper function to format correctly in order to insert the games with years of release 
def splitIntoArray(text_to_split):
    list_of_games = text_to_split.split("\n")
    length_list_of_games = len(list_of_games)

    for i in range(0, length_list_of_games) :
        list_of_games[i] = list_of_games[i].split(" - ")

    for i in range(length_list_of_games-1, -1, -1) :
        if len(list_of_games[i]) != 2:
            list_of_games.pop(i)
        else:
            list_of_games[i][1] = int(list_of_games[i][1])

    return list_of_games

def actuallyInsertingIntoTable():
    my_array = splitIntoArray(nin_games)
    # na verdade dá para usar o comando sql executemany pra insert varias entradas de uma vez numa table 
    for i in range(0, len(my_array)):
        insertIntoTable("my_db.db", my_array[i], "ALL_NINTENDO_GAMES")
    print("finished inserting into ALL_NINTENDO_GAMES")

# createTable("my_db.db", "ALL_NINTENDO_GAMES")
# printAllTablesOfDb("my_db.db")
# actuallyInsertingIntoTable()

def main():
    selectFromTable("my_db.db", "ALL_NINTENDO_GAMES")
main()
 

# sql operators:
# =   Equal
# <>  Not equal. Note: In some versions of SQL this operator may be written as !=
# >   Greater than
# <   Less than
# >=  Greater than or equal
# <=  Less than or equal
# BETWEEN Between a certain range
# LIKE    Search for a pattern
# IN  To specify multiple possible values for a column
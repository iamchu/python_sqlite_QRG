# To test situational stuff... can delete at any moment!
#!/usr/bin/python
import os
import requests
import bs4
import sqlite3 as lite
import sys
import time

## dd/mm/yyyy format
# print (time.strftime("%d/%m/%Y"))
# print ("HI " + time.strftime("%d"))
# print (time.strftime("%m"))
# print (time.strftime("%Y"))

def test():
	print (len(uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("ITAU3.SA")))
	print (type(uol_scraper.scrapeCompanyQuotationsAndReturnAsListOfLists("ITAU3.SA")))

	if 3>7:
		print("its true")

		print("still in?")
	else:
		print ("false")

def howToPrintDataFromTable(db, table):
	pass

def createConnection(db_file):
    """ create a database connection to a SQLite database """
    # when you make a connection to an unexisting db, sqlite creates that db!
    try:
        conn = lite.connect(db_file)
        print(lite.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

def createTable(db, table_name):
	con = lite.connect(db)
	table_name = table_name.replace(".", "_")
	with con:
		cur = con.cursor()
		sqlite_command_drop = "DROP TABLE IF EXISTS "+ table_name
		sqlite_command_create = "CREATE TABLE "+ table_name +"(nome_jogo TEXT, ano_criado INT)"
		cur.execute(sqlite_command_drop)
		cur.execute(sqlite_command_create)
		print("Table " + table_name + " was created.")
	if con:
		con.close()

def makeSqliteDoSomething(db):
	con = lite.connect(db)
	with con:
		cur = con.cursor()
		# From within a C/C++ program (or a script using Tcl/Ruby/Perl/Python bindings) you can get access to table and index names by doing a SELECT on a special table named "SQLITE_MASTER". Every SQLite database has an SQLITE_MASTER table that defines the schema for the database. ... The SQLITE_MASTER table is read-only.
		res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
		for name in res:
		    print (name[0])
	if con:
		con.close()

def splitIntoArray(text_to_split):
	list_of_games = text_to_split.split("\n")
	print(list_of_games[2] + " 1ha")
	length_list_of_games = len(list_of_games)
	for i in range(0, length_list_of_games) :
		list_of_games[i] = list_of_games[i].split(" - ")
	return list_of_games

# x = ["a b"]
# print (x)
# x[0]=x[0].split(" ")
# print (x)

# print (('Stadium Events - 1987').split("-"))
createConnection("minha_bd.db")
createTable("minha_bd.db", "ALL_NINTENDO_GAMES")
createTable("minha_bd.db", "ALL_PS1_GAMES")
makeSqliteDoSomething("minha_bd.db")

print(splitIntoArray("""
Laser Clay Shooting System - 1973
EVR Race - 1975
Wild Gunman - 1976
	"""))
import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create table")
    try:
        sql = """
        CREATE TABLE warehouse
            (w_warehousekey decimal(9,0) not null,
            w_name char(100) not null,
            w_capacity decimal(6,0) not null,
            w_suppkey decimal(9,0) not null,
            w_nationkey decimal(2,0) not null);
        """
        _conn.execute(sql)
        # print("Created Warehouse table")

    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")


def dropTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")
    try:
        sql = """
        DROP TABLE warehouse;
        """
        _conn.execute(sql)
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")





def Q1(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q1")

    

    try:
        

        output = open('output/1.out', 'w')

        header = "{:>10} {:<40} {:>10} {:>10} {:>10}"
        output.write((header.format("wId", "wName", "wCap", "sId", "nId")) + '\n')

        sql = """
        SELECT w_warehousekey as wId, w_name as wName, w_capacity as wCap, w_suppkey as sId, w_nationkey as nId 
            FROM warehouse
            ORDER BY w_warehousekey ASC;
        """
        for row in _conn.execute(sql):
            output.write((header.format(row[0], row[1], row[2], row[3], row[4])) + '\n')

        output.close()
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")



def main():
    database = r"warehouse.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        while True:
            print("=====[ Warehouse Manager ]=====")
            #list options here
            print("1. action")
            print("2. action")
            print("3. action")

            print("Type 'exit' to exit the program")

            print("Please select an option by inputting the corresponding number")
            user_input = str( input("Selection: ") )
            
            if user_input == "1":
                pass
            elif user_input == "2":
                pass
            elif user_input == "exit":
                break
            else:
                print("Invalid selection")


        #call functions here

    closeConnection(conn, database)


if __name__ == '__main__':
    main()

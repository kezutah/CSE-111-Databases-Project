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


def check_shelf_loc(_conn):
    sql = """
        SELECT
            sh_shelfkey
        FROM
            shelf, location, item 
        WHERE
            i_itemkey = lo_itemkey
            AND lo_shelfkey = sh_shelfkey
            AND i_itemkey = ?;
        """
    
    try:
        args = []
        args.append( str(input("Please enter an item key: ")))

        
        print("Shelf Key")
        for row in _conn.execute(sql,args):
            print(row[0])


    except Error as e:
        print(e)

def check_item_qty(_conn):
    # Checks item quantity for one item
    sql = """
            SELECT
                i_quantity
            FROM
                item
            WHERE
                i_itemkey = ?;
        """
    
    try:
        args = []
        args.append( str(input("Please enter an item key: ")))

        
        print("Item Quantity")
        for row in _conn.execute(sql,args):
            print(row[0])


    except Error as e:
        print(e)

def check_order_status(_conn):
    # Checks status of one order for one customer
    sql = """
        SELECT
            o_status
        FROM
            orders
        WHERE
            o_orderkey = ?
            AND o_custkey = ?;
        """
    
    try:
        args = []
        args.append( str(input("Please enter an order key: ")))
        args.append( str(input("Please enter a customer key: ")))

        
        print("Order Status")
        for row in _conn.execute(sql,args):
            print(row[0])


    except Error as e:
        print(e)

def check_all_orders(_conn):
    # Checks date, status, and price total all the orders for any one customer
    sql = """
        SELECT
            *
        FROM
            orders
        WHERE
            o_custkey = ?;
        """
    try:
        args = []
        args.append( str(input("Please enter a customer key: ")))

        
        print("Order # | Date | Status | Total")
        for row in _conn.execute(sql,args):
            print(row[0], row[2], row[3], row[4])


    except Error as e:
        print(e)

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
            print("1. Insert values")
            print("2. Update values")
            print("3. Check values")
            print("4. Delete values")
            print("5. Check tables")
            
            print("'exit' to exit the program")

            print("Please select an option by inputting the corresponding number")
            user_input = str( input("Selection: ") )
            
            if user_input == "1":
                while True:
                    print("What would you like to add?")
                    print("1. Create new product")
                    print("2. Add supplier")
                    print("3. Add new customer")
                    print("4. Create new order")

            elif user_input == "2":
                # update values is not function at the moment
                pass
            elif user_input == "3":

                while True:
                    print("What would you like to check?")
                    print("1. Check shelf location of item")
                    print("2. Check order status")
                    print("3. Check available qty for an item")

                    print("'back' to go back")

                    print("Please select an option by inputting the corresponding number")
                    user_input = str( input("Selection: ") )

                    if user_input == "1":
                        check_shelf_loc(conn)
                        break

                    elif user_input == "2":
                        check_order_status(conn)
                        break

                    elif user_input == "3":
                        check_item_qty(conn)
                        break

                    elif user_input == "back":
                        break

                    else:
                        print("Invalid selection")




            elif user_input == "4":
                # not functional at the moment
                pass
                
            elif user_input == "5":
                # intended to be to look up a table, not just individual elements
                check_all_orders(conn)
            elif user_input == "exit":
                break
            else:
                print("Invalid selection")


        #call functions here

    closeConnection(conn, database)


if __name__ == '__main__':
    main()

import sqlite3
from sqlite3 import Error
from datetime import date


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

def create_customer(_conn):
    try:
        sql = """
        INSERT INTO customer (c_name, c_address, c_amountspent, c_rewardpoints) 
        VALUES (?, ?, 0, 0)"""

        args = []
        args.append( str( input("What is your name? ") ) )
        args.append( str( input("What is your address? ") ) )

        _conn.execute(sql, args)

        sql2 = """
            SELECT
                c_custkey
            FROM
                customer
            WHERE
                c_name = ?;
        """

        for row in _conn.execute(sql2, args[0]):
            return row[0] # returns the customers id numbers

    except Error as e:
        print(e)

def create_order(_conn, custkey):
    sql = """
        INSERT INTO orders (o_custkey, o_orderdate, o_status, o_total)
        VALUES (?, ?, '2-Incomplete', 0)
        """
    sql_check = """
            SELECT
                o_orderkey
            FROM
                orders
            WHERE
                o_custkey = ?
                AND o_orderdate = ?"""
    try:
        args = []
        args.append( str( custkey ) )
        args.append( str( date.today() ) )
        orderkey = None
        for row in _conn.execute(sql_check, args):
            orderkey = row[0]
        if type(orderkey) == type(1):
            pass
        else:
            _conn.execute(sql, args)
            for row in _conn.execute(sql_check, args):
                orderkey = row[0] # by now we have an order created with an orderkey available
    except Error as e:
        print(e)

def add_supplier(_conn):
    sql = """
        INSERT INTO
            supplier (sp_suppkey, sp_name, sp_address, sp_notes)
        VALUES
            (?,?,?,?);
        """
    
    try:
        args = []
        args.append( str(input("Enter supplier key: ")))
        args.append( str(input("Enter supplier name: ")))
        args.append( str(input("Enter supplier address: ")))
        args.append( str(input("Enter supplier notes: ")))
        
        _conn.execute(sql,args)
        _conn.commit()
        
        print("Added supplier " + args[1])
        


    except Error as e:
        print(e)

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

def check_avail_item(_conn):
    sql = """
        SELECT
            i_itemkey, i_quantity, i_type, i_color
        FROM
            item
        WHERE
            i_quantity > 0;
        """
    
    try:
        print("Item # | Quantity | type | Color")
        for row in _conn.execute(sql):
            print(row[0], row[2], row[3], row[4])

    except Error as e:
        print(e)

def check_item_qty(_conn, itemkey=0):
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
        if(itemkey == 0):
            args.append( str(input("Please enter an item key: ")))

            
            print("Item Quantity")
            for row in _conn.execute(sql,args):
                print(row[0])
        else:
            args.append(str(itemkey))
            for row in _conn.execute(sql,args):
                return(row[0])


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

def check_all_orders(_conn, custkey=0):
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
        if custkey == 0:
            args.append( str(input("Please enter a customer key: ")))
        
        else:
            args.append(custkey)

        print("Order # | Date | Status | Total")
        for row in _conn.execute(sql,args):
            print(row[0], row[2], row[3], row[4])


    except Error as e:
        print(e)

def create_item(_conn):
    sql = """
        INSERT INTO
            item (i_itemkey, i_suppkey, i_quantity, i_type, i_color, i_price)
        VALUES
            (?,?,?,?,?,?);
        """
    
    try:
        args = []
        args.append( str(input("Enter new itemkey: ")))
        args.append( str(input("Please enter a supplier key: ")))
        args.append( str(input("Please enter item's quantity: ")))
        args.append( str(input("Please enter item's type: ")))
        args.append( str(input("Please enter item's color: ")))
        args.append( str(input("Please enter item's price: ")))


        _conn.execute(sql,args)
        _conn.commit()
        print("Item Created")
        
        itemkey = args[0]
        
        print("Please select where to place the item")
        
        sql = """
            UPDATE
                location, shelf, item
            SET
                sh_shelfkey = ?,
                lo_lockey = ?,
                lo_shelfkey = ?
            WHERE
                i_itemkey = lo_itemkey
                AND sh_shelfkey = lo_shelfkey
                AND i_itemkey = ?;
        """

        args = []
        args.append( str(input("Please enter a shelf key: ")))
        args.append( str(input("Please enter a location key: ")))
        args.append(args[0])
        args.append(itemkey)

        _conn.execute(sql,args)
        _conn.commit()
        print("Item stored at location " + args[1] + ", shelf " + args[0])

        


    except Error as e:
        print(e)

def change_item_location(_conn):
    sql = """
            UPDATE
                location, shelf, item
            SET
                sh_shelfkey = ?,
                lo_lockey = ?,
                lo_shelfkey = ?
            WHERE
                i_itemkey = lo_itemkey
                AND sh_shelfkey = lo_shelfkey
                AND sh_shelfkey = ?
                AND lo_lockey = ?
                AND i_itemkey = ?;
        """
    
    try:
        args = []
        args.append( str(input("Please enter a new shelf key: ")))
        args.append( str(input("Please enter a new location key: ")))
        args.append(args[0])
        args.append( str(input("Please enter the old shelf key: ")))
        args.append( str(input("Please enter the old location key: ")))
        args.append( str(input("Please enter the item's key: ")))

        _conn.execute(sql,args)
        _conn.commit()
        print("Item successfully moved to shelf " + args[0] + " at location " + args[1])

    except Error as e:
        print(e)

def edit_item_quantity(_conn, amount=0, itemkey=0):
    # Edits a given item's quantity.
    # If this function is called with given arguments, simply executes the command
    # Otherwise, prompts the user for a specific item_id or an amount
    sql = """
        UPDATE
            item
        SET
            i_quantity  = (
                SELECT
                    i_quantity
                FROM
                    item
                WHERE
                    i_itemkey = 1
            ) + ?
        WHERE
            i_itemkey = 1;
        """ # for the filling information, the 1st and 3rd argument are the item_id and the 2nd
            # is the amount that we need to add (negative number if subtracting)

    try:
        args = []
        run = True
        if(amount==0 and itemkey ==0):
            while(True):
                itemkey = str(input("Please enter a item key: "))
                amount = str(input("Please enter how much to add or subtract: "))
                current_amount = check_item_qty(_conn, itemkey)
                if(amount > 0 or (amount < 0 and current_amount > abs(amount))):
                    args.append( itemkey )
                    args.append( amount )
                    args.append( itemkey )
                    break
                elif(amount < 0 and current_amount < abs(amount)):
                    print("Insufficient quantity available.")
                else:
                    run = False


        
        if(run == True):
            print("Item Quantity")
            for row in _conn.execute(sql,args):
                print(row[0])
        else:
            print("Something went wrong.")

    
    except Error as e:
        print(e)

def edit_order_status (_conn):
    sql = """
        UPDATE
            orders
        SET
            o_status = ?
        WHERE
            o_orderkey = ?
            AND o_custkey = ?;
        """
    
    try:
        args = []
        args.append( str(input("Enter new order status: ")))
        args.append( str(input("Please enter an order key: ")))
        args.append( str(input("Please enter a customer key: ")))

        _conn.execute(sql,args)
        _conn.commit()
        print("Order Status Updated")
        


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
        login = str( input("Are you entering as a 'c'ustomer or 'a'dmin? ") )
        if(login.lower() == 'a'):
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
                    
                        print("'back' to go back")

                        print("Please select an option by inputting the corresponding number")
                        user_input = str( input("Selection: ") )

                        if user_input == "1":
                            create_item(conn)
                            break

                        elif user_input == "2":
                            add_supplier(conn)
                            break

                        elif user_input == "back":
                            break

                        else:
                            print("")

                elif user_input == "2":
                    while True:
                        print("What would you like to edit?")
                        print("1. Edit item quantity")
                        print("2. Edit shelf location")
                        print("3. Edit order status")

                        print("'back' to go back")
                        
                        print("Please select an option by inputting the corresponding number")
                        user_input = str( input("Selection: ") )

                        if user_input == "1":
                            edit_item_quantity(conn)
                            break

                        elif user_input == "2":
                            change_item_location(conn)
                            break

                        elif user_input == "3":
                            edit_order_status(conn)

                        elif user_input == "back":
                            break

                        else:
                            print("Invalid selection")

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
        elif(login.lower() == 'c'):
            print("Hello customer. What would you like to do?")
            print("What is your customer_id?")
            id = input( str( "If you are a new customer, please type '0': "))
            if id == 0:
                    # make a new customer entity for this person
                    id = create_customer(conn)
            while True:
                print("1. See what products are available")
                print("2. Order a product")
                print("3. Check on your order's status")

                print("'exit' to exit the program")

                print("Please select an option by inputting the corresponding number")
                user_input = str( input("Selection: ") )

                if user_input == "1":
                    check_avail_item(conn)

                elif user_input == "2":
                    create_order(conn, id)

                elif user_input == "3":
                    check_all_orders(conn, id)

                elif user_input == "exit":
                    break

    closeConnection(conn, database)


if __name__ == '__main__':
    main()

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

def create_order(_conn, custkey=0):
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
                AND o_orderdate = ?
            """
    
    sql_line = """
            INSERT INTO lineitem (l_orderkey, l_itemkey, l_quantity, l_subtotal, l_discount)
            VALUES (?, ?, ?, ?, ?)"""
    
    sql_line_update = """
            UPDATE
                lineitem
            SET
                l_subtotal = (
                    SELECT sum(i_price*l_quantity)
                    FROM lineitem, item
                    WHERE l_orderkey = ? AND l_itemkey = i_itemkey
                )
            WHERE
                l_orderkey = ?;
            """
    
    sql_order_update = """
                    UPDATE
                        orders
                    SET
                        o_total = (
                            SELECT sum(l_subtotal*(1-l_discount) )
                            FROM lineitem
                            WHERE l_orderkey = ?
                        )
                    WHERE
                        o_orderkey = ?;
                    """
    
    try:
        args = []
        if custkey == 0:
            custkey = input( str("Please type in a customer key: ") )
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
        
        # create line items to this orderkey
        while(True):
            args.clear()
            args.append( str( orderkey) )
            args.append( str( input("What item (itemkey) would you like to buy? ") ) )
            args.append( str( input("How many would you like to purchase? ") ) )
            avail_qty = check_item_qty(_conn, args[1])
            while( avail_qty < int( args[1] ) ):
                print("There is not enough stock available. There are only " + avail_qty + " available.")
                args[1] = str( input("How many would you like to purchase? ") )
            args.append( str(0) )
            args.append( str(0) )

            _conn.execute(sql_line, args)
            
            again = input("Would you like to order another item (Y / N)? ").lower()
            if again == 'y':
                pass
            elif again == 'n':
                break

        # After all the line items were created, tally up their subtotals
        args.clear()
        # fill the args with 2 orderkeys
        args.append( str( orderkey ) )
        args.append( str( orderkey ) )
        _conn.execute(sql_line_update, args)

        # After all the line items are subtotaled, tally up the order's total
        _conn.execute(sql_order_update, args) # args still has 2 orderkeys, which is all we need for this query
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
                        print("3. Add new customer")
                        print("4. Create new order")
                    
                        print("'back' to go back")

                        print("Please select an option by inputting the corresponding number")
                        user_input = str( input("Selection: ") )

                        if user_input == "1":
                            edit_item_quantity(conn)
                            break

                        elif user_input == "2":
                            break

                        elif user_input == "3":
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
                            break

                        elif user_input == "3":
                            break

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

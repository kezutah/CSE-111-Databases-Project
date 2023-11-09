-- create new product
INSERT INTO item (i_itemkey, i_suppkey, i_quantity, i_type, i_color)
VALUES(1,1,10,'shampoo', 'red');

--add supplier 
INSERT INTO supplier (sp_suppkey, sp_name, sp_address, sp_notes)
VALUES(1,'Supplier 1', '123 Example Street', 'first supplier');

--create new customer
INSERT INTO customer (c_custkey, c_name, c_address, c_rewardpoints, c_notes)
VALUES(1,'John Smith', '321 Customer Street', 0, 'first customer');

--edit available item quantity for a specific item
UPDATE item
    SET i_quantity  = 1
    WHERE i_itemkey = 1;


--update order total based on each lineitem price
UPDATE orders
    SET o_total = (
        SELECT sum(l_subtotal*(1-l_discount) )
        FROM lineitem
        WHERE l_orderkey = 1
    )
    WHERE o_orderkey = 1;

--create new order
INSERT INTO orders (o_orderkey, o_custkey, o_orderdate, o_status, o_total, o_notes)
VALUES (1,1,'4-19-2023','incomplete', 0, 'new order');

--create new transfer
INSERT INTO transfer (t_trankey, t_storekey, t_orderdate, t_status, t_notes)
VALUES (1,1,'4-19-2023','incomplete', 'new transfer');

--add lineitem to order
INSERT INTO lineitem (l_linekey, l_orderkey, l_trankey, l_itemkey, l_quantity, l_subtotal, l_discount, l_notes)
VALUES (1,1,NULL,1,10,5,.1,'order lineitem');

--add lineitem to transfer
INSERT INTO lineitem (l_linekey, l_orderkey, l_trankey, l_itemkey, l_quantity, l_subtotal, l_discount, l_notes)
VALUES (1,NULL,1,1,10,5,.1,'transfer lineitem');

--submit an order and change its status
UPDATE orders
    SET o_status = 'submitted'
    WHERE o_orderkey = 1
        AND o_custkey = 2 
        AND o_status = 'incomplete';

--submit a transfer and change its status
UPDATE transfer
    SET t_status = 'submitted'
    WHERE t_trankey = 1
        AND t_storekey = 2 
        AND t_status = 'incomplete';

--check order status
SELECT o_status
    FROM orders
    WHERE o_orderkey = 1
        AND o_custkey = 1;

--check shelf location of item
SELECT sh_shelfkey
    FROM shelf, location, item 
    WHERE i_itemkey = lo_itemkey
        AND lo_shelfkey = sh_shelfkey
        AND i_itemkey = 1;


--change shelf location of item
UPDATE location, shelf
    SET sh_shelfkey = 1,
        lo_lockey = 2,
        lo_shelfkey = 1
    WHERE sh_shelfkey = lo_shelfkey
        AND lo_lockey = 3
        AND sh_shelfkey = 4;

--check quantity available for an item
SELECT i_quantity
    FROM item
    WHERE i_itemkey = 1;
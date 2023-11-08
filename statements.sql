-- create new product
INSERT INTO item (i_itemkey, i_suppkey, i_quantity, i_type, i_color)
VALUES(1,1,10,'shampoo', 'red');

--add supplier 
INSERT INTO supplier (sp_suppkey, sp_name, sp_address, sp_notes)
VALUES(1,'Supplier 1', '123 Example Street', 'first supplier');



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

--add lineitem to order
INSERT INTO lineitem (l_linekey, l_orderkey, l_trankey, l_itemkey, l_quantity, l_subtotal, l_discount, l_notes)
VALUES (1,1,1,1,10,5,.1,'lineitem');

--submit an order and change its status
UPDATE orders
    SET o_status = 'submitted'
    WHERE o_orderkey = 1
        AND o_custkey = 1 
        AND o_status = 'incomplete';

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

--check quantity available for an item
SELECT i_quantity
    FROM item
    WHERE i_itemkey = 1;
import pyodbc


server = ''
database = ''
uID = ''
pWD = ''



def connectdb():
    global connection, cursor
    connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={uID};PWD={pWD}')
    cursor = connection.cursor()

def keyCounter(key):
    cursor.execute("UPDATE L_Keys SET USAGE_COUNT = USAGE_COUNT + 1 where KEYS = (?)",(key,))
    connection.commit()
    print("Key Usage")


def add_LicenceKey(key, duration,enddate):  # Inputlar 1, 6, 12 ay şeklinde zaman tabanlı olacak
    cursor.execute(f"INSERT INTO L_Keys (KEYS, ENDDATE, DURATION,ACTIVATED,USAGE_COUNT) VALUES (?,?,?, 1,0)",(key,enddate,duration))
    connection.commit()
    
def pull_LicenceKey(key):
    return cursor.execute(f"select * from L_Keys where Keys = '{key}'").fetchone()
    
def add_Product(link, size, usermail):
    # cursor = connectdb()
    print("add_Product\n")
    
    if cursor.execute(f"SELECT * FROM Product Where Product = '{link}'").fetchone():
        print("Product already exists")
    else:
        cursor.execute(f"INSERT INTO Product (Product) VALUES (?)", (link,))

    product_ID = cursor.execute(f"SELECT ID FROM Product WHERE Product = '{link}'").fetchone()

    if cursor.execute(f"SELECT * FROM Size WHERE Product_ID = '{product_ID[0]}' AND Size = '{size}'").fetchone():
        print("Size already exists")
    else:
        cursor.execute(f"INSERT INTO Size (Product_ID,Size,In_Stock) VALUES (?,?,?)",(product_ID[0],size.upper(),False))
        connection.commit()

    Size_ID = cursor.execute(f"SELECT ID FROM Size WHERE Product_ID = '{product_ID[0]}' AND Size = '{size}'").fetchone()
    
    if cursor.execute(f"SELECT * FROM mails WHERE Size_ID = '{Size_ID[0]}' AND Mail = '{usermail}'").fetchone():
        print("Mail already exists")
    else:
        cursor.execute(f"INSERT INTO mails (Size_ID,Mail) VALUES (?,?)",(Size_ID[0],usermail))
    
    connection.commit()

def pull_Product_Flex(table,find,row,sort):
    
    return cursor.execute(f"SELECT {find} FROM {table} WHERE {row} = ?",(sort,)).fetchall()

def pull_Product(table,find):
    # cursor = connectdb()
    
    return cursor.execute(f"SELECT {find} FROM {table}").fetchall()

def update_Product(name,price,sizes):
    cursor.executemany(f"UPDATE Size set In_Stock = ? WHERE ID = ?",[(x[3], x[0]) for x in sizes])
    cursor.execute(f"UPDATE Product set [Product Name] = ?, NewPrice = ? WHERE ID = ?",(name,price,sizes[0][1]))
    connection.commit()
    print("Updated")


def pull_mails(ids):
    ids = ids[0]
    query = "SELECT * FROM mails WHERE Size_ID IN ({})".format(','.join(['?'] * len(ids)))
    cursor.execute(query, ids)
    return cursor.fetchall()


def pull_products_for_mail():

    query = """	
        SELECT 
            p.Product, 
            s.Size,
            m.Mail,
            m.Size_ID,
            s.Product_ID,
            p.[Product Name],
            p.NewPrice
        FROM Product p
        JOIN Size s ON p.ID = s.Product_ID and In_Stock = 1
        JOIN Mails m ON s.ID = m.Size_ID;
 """


    cursor.execute(query)
    return cursor.fetchall()





def delete_Size(Size_ID,Product_ID):
    cursor.execute(f"DELETE FROM Size WHERE ID = {Size_ID}")
    connection.commit()
    
    if cursor.execute(f"SELECT * FROM Size WHERE Product_ID = '{Product_ID}'").fetchone() == None:
        print("Ürün Silindi. ID = ",Product_ID)
        cursor.execute(f"DELETE FROM Product WHERE ID = {Product_ID}")
        connection.commit()
    else:
        print("Ürün halen mevcut.")





def delete_Product(id):
    cursor.execute(f"DELETE FROM Product WHERE ID = {id}")
    connection.commit()


def close_Connection():
    cursor.close()
    connection.close()  
import mysql.connector


def insert_data(symbol, price, timestamp):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Binance_opa3",  # Remplacez par votre mot de passe MySQL
        database="crypto_prices"  # Nom de votre base de données
    )

    cursor = conn.cursor()

    query = "INSERT INTO crypto_data (symbol, price, timestamp) VALUES (%s, %s, %s)"
    query2 = "INSERT INTO traders_data (symbol, id_trade, price, qty, time) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (symbol, price, timestamp))
    cursor.execute(query2, (symbol, id_trade, price, qty, time))

    conn.commit()
    cursor.close()
    conn.close()

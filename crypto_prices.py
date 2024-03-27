import requests
import csv
import time
from datetime import datetime
import schedule
import mysql.connector
import logging

# Configuration de la connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Binance_opa3",
    database="crypto_prices"
)
cursor = conn.cursor()

# Configuration du logging
logging.basicConfig(filename='crypto_prices.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_data(symbol, data_type):
    """
    Fonction pour récupérer des données à partir de l'API Binance.
    """
    base_url = "https://api.binance.us"

    if data_type == "price":
        endpoint = "/api/v3/ticker/price"
    elif data_type == "order_book":
        endpoint = "/api/v3/depth"
    else:
        raise ValueError("Type de données non valide : " + data_type)

    params = {
        "symbol": symbol,
    }

    response = requests.get(base_url + endpoint, params=params)

    if response.status_code != 200:
        error_message = f"Requête API a échoué avec le code {response.status_code}: "
        try:
            error_data = response.json()
            error_message += error_data.get('msg', 'Aucun message d\'erreur spécifié.')
        except:
            error_message += 'Impossible de récupérer le message d\'erreur.'
        logging.error(error_message)
        raise RuntimeError(error_message)

    data = response.json()
    return data["price"]


def append_crypto_data_to_db(symbol, cursor):
    """
    Fonction pour ajouter les valeurs des 3 dernières heures de la crypto BTCUSDT dans une table de la base de données.
    """
    current_timestamp = int(time.time()) * 1000
    three_hours_ago_timestamp = current_timestamp - (3 * 60 * 60 * 1000)

    while current_timestamp >= three_hours_ago_timestamp:
        timestamp_seconds = current_timestamp // 1000
        dt_object = datetime.fromtimestamp(timestamp_seconds)
        formatted_datetime = dt_object.strftime("%Y-%m-%d %H:%M:%S")

        price = get_data(symbol, "price")

        insert_query = "INSERT INTO crypto_data (symbol, price, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (symbol, price, formatted_datetime))
        conn.commit()

        current_timestamp -= 60000
        time.sleep(0.5)


def execute_task():
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT", "DOTUSDT", "SOLUSDT", "DOGEUSDT", "LTCUSDT","UNIUSDT"]

    for symbol in symbols:
        try:
            append_crypto_data_to_db(symbol, cursor)
        except Exception as e:
            logging.error(f"Erreur lors de l'insertion des données pour le symbole {symbol}: {e}")


schedule.every(5).minutes.do(execute_task)

while True:
    schedule.run_pending()
    time.sleep(1)
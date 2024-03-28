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
logging.basicConfig(filename='traders_data.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_traders(symbol, limit=1000):
    """
    Récupère les données des traders pour un symbole donné.

    Args:
        symbol (str): Le symbole de la crypto-monnaie (ex: "BTCUSDT").
        limit (int, optionnel): Le nombre maximum de trades à récupérer (défaut: 1000).

    Returns:
        list: Une liste de dictionnaires représentant les trades.
    """
    api_url = "https://api.binance.us/api/v1/trades"
    params = {
        "symbol": symbol,
        "limit": limit
    }

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Erreur lors de la récupération des traders pour le symbole {symbol}: {response.status_code}")
        return None

def append_traders_data_to_db(symbol, cursor):
    """
    Ajoute les données des traders à la base de données.

    Args:
        symbol (str): Le symbole de la crypto-monnaie.
        cursor: Le curseur de la base de données.
    """
    traders = get_traders(symbol)
    if traders:
        for trade in traders:
            trade_time = datetime.utcfromtimestamp(int(trade['time']) // 1000).strftime('%Y-%m-%d %H:%M:%S.%f')
            insert_query = "INSERT INTO traders_data (Symbol, id, price, qty, quoteQty, time, isBuyerMaker, isBestMatch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (symbol, trade['id'], trade['price'], trade['qty'], trade['quoteQty'], trade_time, trade['isBuyerMaker'], trade['isBestMatch']))
            conn.commit()

def execute_traders_task():
    """
    Exécute la tâche de récupération des données des traders.
    """
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT", "DOTUSDT", "SOLUSDT", "DOGEUSDT", "LTCUSDT", "UNIUSDT"]

    for symbol in symbols:
        try:
            append_traders_data_to_db(symbol, cursor)
        except Exception as e:
            logging.error(f"Erreur lors de l'insertion des données des traders pour le symbole {symbol}: {e}")

# Démarrage de la tâche
schedule.every(5).minutes.do(execute_traders_task)

while True:
    schedule.run_pending()
    time.sleep(1)

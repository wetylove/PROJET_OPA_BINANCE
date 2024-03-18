import pandas as pd
from datetime import datetime, timedelta
import requests
import time

def get_historical_data(symbol, start_time):
    """
    Fonction pour récupérer les données historiques du BTC-USDT pour les 3 dernières heures.

    Args:
        symbol (str): Symbole du marché (par exemple, "BTCUSDT").
        start_time (int): Timestamp UNIX en millisecondes pour l'heure de début des données historiques.

    Returns:
        pd.DataFrame: DataFrame contenant les données historiques du symbole.
    """
    base_url = "https://api.binance.us"
    endpoint = "/api/v3/klines"

    # Convertir le timestamp en millisecondes en secondes
    start_time_seconds = start_time // 1000

    # Calculer l'heure actuelle moins 3 heures
    end_time_seconds = datetime.now().timestamp() - 3 * 3600

    params = {
        "symbol": symbol,
        "interval": "1h",  # Interval d'une heure
        "startTime": int(start_time_seconds),
        "endTime": int(end_time_seconds * 1000),  # Convertir en millisecondes
        "limit": 1000  # Limite maximale de données
    }

    response = requests.get(base_url + endpoint, params=params)

    if response.status_code != 200:
        raise RuntimeError("Requête API a échoué avec le code {}".format(response.status_code))

    data = response.json()

    # Convertir les données en DataFrame
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time",
                                      "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
                                      "taker_buy_quote_asset_volume", "ignore"])

    # Convertir le timestamp en datetime et fixer l'index
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    return df

# Déterminer l'heure de début des données historiques (3 heures avant maintenant)
start_time = datetime.now() - timedelta(hours=3)

# Appeler la fonction pour récupérer les données historiques
symbol = "BTCUSDT"
df = get_historical_data(symbol, start_time.timestamp() * 1000)  # Convertir en millisecondes

# Afficher le DataFrame
print(df)

# Sauvegarder les données dans un fichier CSV en temps réel
filename = "historical_data_BTCUSDT.csv"
while True:
    df.to_csv(filename)
    print("Données enregistrées dans", filename)
    # Attendre 1 heure avant de mettre à jour le fichier CSV
    
    time.sleep(3600)

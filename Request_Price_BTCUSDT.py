import requests

def get_data(symbol, data_type):
    """
    Fonction pour récupérer des données à partir de l'API Binance.

    Args:
        symbol (str): Symbole du marché (par exemple, "BTC-USDT").
        data_type (str): Type de données ("price" ou "order_book").

    Returns:
        dict: Dictionnaire contenant les données récupérées.
    """
    # URL de base de l'API Binance
    base_url = "https://api.binance.us"

    # Déterminer l'endpoint en fonction du type de données
    if data_type == "price":
        endpoint = "/api/v3/ticker/price"
    elif data_type == "order_book":
        endpoint = "/api/v3/depth"
    else:
        raise ValueError("Type de données non valide : " + data_type)

    # Paramètres de la requête
    params = {
        "symbol": symbol,
    }

    # Envoyer la requête et obtenir la réponse
    response = requests.get(base_url + endpoint, params=params)

    # Vérifier le code de statut de la réponse
    if response.status_code != 200:
        error_message = "Requête API a échoué avec le code {}: ".format(response.status_code)
        try:
            error_data = response.json()
            error_message += error_data.get('msg', 'Aucun message d\'erreur spécifié.')
        except:
            error_message += 'Impossible de récupérer le message d\'erreur.'
        raise RuntimeError(error_message)

    # Analyser la réponse JSON
    data = response.json()

    # Retourner les données
    return data

# Exemple d'utilisation avec un symbole de marché valide
symbol = "BTCUSDT"  # Utilisez un symbole de marché valide (sans tiret)
data_type = "price"

try:
    data = get_data(symbol, data_type)
    print(data)
except Exception as e:
    print("Une erreur s'est produite:", e)

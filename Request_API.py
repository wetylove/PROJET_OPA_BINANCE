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
  base_url = "https://api.binance.com"

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
    raise RuntimeError("Requête API a échoué : " + str(response.status_code))

  # Analyser la réponse JSON
  data = response.json()

  # Retourner les données
  return data

# Exemple d'utilisation
symbol = "BTC-USDT"
data_type = "price"

data = get_data(symbol, data_type)

# Imprimer les données
print(data)
import requests

class PokeAPIClient:
    """Maneja la conexión y obtención de datos e imágenes desde PokeAPI."""
    
    @staticmethod
    def get_pokemon_data(pokemon_name_or_id):
        url = f"https://pokeapi.co/api/v2/pokemon/{str(pokemon_name_or_id).lower()}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
                return {
                    "name": data['name'],
                    "sprite_url": data['sprites']['front_default'],
                    "hp": stats.get('hp', 50),
                    "speed": stats.get('speed', 50),
                    "attack": stats.get('attack', 50)
                }
        except Exception as e:
            print(f"Error al conectar con PokeAPI: {e}")
        return None

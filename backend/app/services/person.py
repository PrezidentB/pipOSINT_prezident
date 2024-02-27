from app.utils.Requester import Requester
from app.utils.tools import get_countries, get_country

def get_person_info(firstname: str, lastname: str) -> tuple:

        # Initialisation des variables de sortie
        output_gender = {"value": None, "probability": None}
        output_country = None

        # Nationalize
        params = {
            "name": f"{firstname.lower()}"
        }
        response = Requester(url=f"https://api.genderize.io", params=params).get()
        if response and response.status_code == 200:
            parsed = response.json()
            output_gender["value"] = parsed['gender']
            output_gender["probability"] = parsed['probability']

        # Genderize
        params = {
            "name": f"{firstname.lower()}"
        }
        response = Requester(url=f"https://api.nationalize.io", params=params).get()
        if response and response.status_code == 200:
            parsed = response.json()
            output_country = parsed['country']

            countries = get_countries()

            for country in output_country:
                country['name'], country['flag'] = get_country(countries, country['country_id'])
                del country['country_id']

        return output_gender, output_country
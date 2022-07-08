import requests
import json
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()




if __name__ == '__main__':
    configure()

    api_key = os.getenv('api_key')
    email = os.getenv('email')





    request_link = 'https://vrdb-tc-apicast-production.api.canada.ca/eng/vehicle-recall-database/v1/recall/make-name/toyota/model-name/camry/year-range/2005-2005'
    header = {"Accept": "application/json", "user-key": api_key }
    response = requests.get(request_link, headers=header, auth=(email, api_key))
    print(response.json())
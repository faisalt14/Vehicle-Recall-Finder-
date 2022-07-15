from curses import raw
import requests
import json
from dotenv import load_dotenv
import os



def configure():
    load_dotenv()

def get_json(): 
    
    api_key = os.getenv('api_key')
    email = os.getenv('email')





    request_link = 'https://vrdb-tc-apicast-production.api.canada.ca/eng/vehicle-recall-database/v1/recall/make-name/honda/model-name/civic/year-range/2002-2002'
    header = {"Accept": "application/json", "user-key": api_key }
    response = requests.get(request_link, headers=header, auth=(email, api_key))   
    get_json.var = response.json() # raw JSON dictionary
    # print(response.json())


def format_json():
    total_recalls = len(get_json.var["ResultSet"])
    raw_json = get_json.var

    print()
    print("                                           RESULTS                                                 ")    
    print("---------------------------------------------------------------------------------------------------")




    for recall in range(total_recalls): 

        vehicle_make = raw_json["ResultSet"][recall][3]["Value"]["Literal"]
        vehicle_model= raw_json["ResultSet"][recall][2]["Value"]["Literal"]
        vehicle_year = raw_json["ResultSet"][recall][4]["Value"]["Literal"]
        recall_num = int(raw_json["ResultSet"][recall][0]["Value"]["Literal"])
        recall_date = raw_json["ResultSet"][recall][5]["Value"]["Literal"]
        recall_date = recall_date[:9] # removed time


        print()
        print(f"[{recall+1}]") 
        print("---------------------------------------------------------------------------------------------------")
        print("|    Make    |   |    Model    |   |    Year    |   |    Recall Number   |   |   Recall Date   |   ")
        print()
        print("|", "   " + vehicle_make, " "*(6-len(vehicle_make)), "|", "  |", "   " + vehicle_model, " "*(7-len(vehicle_model)), "|", "  |", "   " + vehicle_year, " "*(6-len(vehicle_year)), "|", "  |", "   " + str(recall_num), " "*(14-len(str(recall_num))), "|", "  |", "   " + recall_date, " "*(11-len(recall_date)), "|"  )
        print()

        


        

        # print("Recall Number:",  recall_num)
        # print("Recall Date: " + recall_date)

        









if __name__ == '__main__':
    configure()
    get_json()
    


    format_json()
from curses import raw
from typing_extensions import Self
import requests
import json
from dotenv import load_dotenv
import os




class RecallApp: 

    def __init__(self) -> None:
        self.make = ""
        self.model = ""
        self.year = ""

        self.api_key = None
        self.email = None
        self.rawJson = None

        
        

    def configure(self):
        load_dotenv()

    def prompt(self):

        self.make = input("Please enter the make of the vehicle: ")
        self.model = input("Please enter the model name: ")
        self.year= input("Please enter the year range (Ex: 2002-2004): " )
        
        


    def get_json(self): 
        
        self.api_key = os.getenv('api_key')
        self.email = os.getenv('email')



        # request_link = 'https://vrdb-tc-apicast-production.api.canada.ca/eng/vehicle-recall-database/v1/recall/make-name/honda/model-name/civic/year-range/2002-2002'
        request_link = f'https://vrdb-tc-apicast-production.api.canada.ca/eng/vehicle-recall-database/v1/recall/make-name/{self.make}/model-name/{self.model}/year-range/{self.year}'
        print(request_link)
        header = {"Accept": "application/json", "user-key": self.api_key }
        response = requests.get(request_link, headers=header, auth=(self.email, self.api_key))   
        self.rawJson = response.json() # raw JSON dictionary
        # print(response)



    def get_summary(self, recall_num: int) -> str:
        recall_num = recall_num
        

        api_key = os.getenv('api_key')
        email = os.getenv('email')





        request_link = f'https://vrdb-tc-apicast-production.api.canada.ca/eng/vehicle-recall-database/v1/recall-summary/recall-number/{recall_num}'
        header = {"Accept": "application/json", "user-key": self.api_key }
        response = requests.get(request_link, headers=header, auth=(self.email, self.api_key))   
        self.rawJson = response.json() # raw JSON dictionary
        raw_json = self.rawJson
        # print(response.json())


        summary = raw_json["ResultSet"][0][11]["Value"]["Literal"] + """ """
        return summary



    def format_json(self):
        total_recalls = len(self.rawJson["ResultSet"])
        raw_json = self.rawJson

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
            print()


            text = "Summary"
            underlined_text = "\x1B[4m" + text + "\x1B[0m"
            print(underlined_text) 
            print()

            summary = self.get_summary(recall_num)
            print(summary)

            


        

        





if __name__ == '__main__':

    app = RecallApp()

    

    app.configure()

    app.prompt()
    app.get_json()
    app.format_json()

    
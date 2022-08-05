from curses import raw
from tabnanny import check
from typing_extensions import Self
import requests
import json
from dotenv import load_dotenv
import os




class RecallApp: 

    def __init__(self) -> None:

        self.configure()


        self.make = ""
        self.model = ""
        self.year = ""

        self.api_key = os.getenv('api_key')
        self.email = os.getenv('email')
        self.rawJson = None


        self.year_flag = False
        self.make_flag = False
        self.model_flag = False

        

    def configure(self):
        load_dotenv()

    def prompt(self):

        
        while len(self.make) == 0: 
            self.make = input("Please enter the make of the vehicle: ")



        while len(self.model) == 0:     
            self.model = input("Please enter the model name: ")


                
        while len(self.year) != 9:
            self.year= input("Please enter the year range (Ex: 2002-2004): " )    

        self.year_flag = self.check_year()

        while self.year_flag != True: 
            self.year= input("Please enter the year range (Ex: 2002-2004): " )
            self.year_flag = self.check_year()
             




    def check_year(self) -> bool: 


        if len(self.year) != 9: 
            return False

        else:    
            
            self.year_flag = False

            year1 = self.year[:4]
            dash = self.year[4]
            year2 = self.year[5:]        

            if year1.isnumeric() and dash == "-" and year2.isnumeric():
            
                if int(year1) > int(year2): 
                    print("The first year must be smaller than the second year in the range.")
                    
                    self.year_flag = False
                else: 
            
                    self.year_flag = True    

            return self.year_flag




    def get_json(self): 
        

        request_link = f'https://vrdb-tc-apicast-production.api.canada.ca/eng/vehicle-recall-database/v1/recall/make-name/{self.make}/model-name/{self.model}/year-range/{self.year}'
        header = {"Accept": "application/json", "user-key": self.api_key }
        response = requests.get(request_link, headers=header, auth=(self.email, self.api_key))   
        self.rawJson = response.json() # raw JSON dictionary
        

        


    def get_summary(self, recall_num: int) -> str:
        recall_num = recall_num
        


        request_link = f'https://vrdb-tc-apicast-production.api.canada.ca/eng/vehicle-recall-database/v1/recall-summary/recall-number/{recall_num}'
        header = {"Accept": "application/json", "user-key": self.api_key }
        response = requests.get(request_link, headers=header, auth=(self.email, self.api_key))   
        self.rawJson = response.json() # raw JSON dictionary
        raw_json = self.rawJson



        summary = raw_json["ResultSet"][0][11]["Value"]["Literal"] + """ """
        return summary



    def format_json(self):
        total_recalls = len(self.rawJson["ResultSet"])
        raw_json = self.rawJson

        if total_recalls == 0: 
            print()
            print("No recalls found!")
            print()

        else: 
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
                print()

            


        

        





if __name__ == '__main__':

    app = RecallApp()



    app.prompt()


    app.get_json()
    app.format_json()

    
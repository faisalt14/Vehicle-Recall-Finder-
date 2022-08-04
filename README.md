# Vehicle-Recall-Finder-


Vehicle Recall Finder is an application Canadians can use to determine whether their vehicle has a recall placed on it. 

The application prompts users to enter in a vehicle make, model, and the year range for which they wish to see. Ex. Honda Civic 2012-2015. The results are then displayed in text format. Each result will be numbered and include the recall number, summary, and date posted. 

In order to use the application the user must have the python programming language, an IDE, and requests module downloaded. The python requests module allows us to make HTTP requests to a server, in this case the Government of Canada API store. Users will also be required to make a free account on the API store website https://api.canada.ca/en/homepage#all-apis . After creating an account, users will be provided with a unique API key. 

To run the application, users can pull the repository from Github, then add the file: 
.env to the src directory and include the following lines of code: 

email=example@gmail.com # insert the email associated with your API store account 
api_key=exampleexampleexample # insert your API key. 

(A .env file is used to prevent sensitive credentials such as API keys and email addresses being included in version control and public repositories.)

Then, users can run the application and check if their vehicle has a recall, hopefully it doesn't!


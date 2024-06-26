from flask_restful import Resource, Api # import the Resource class from the flask_restful module
from flask import Flask, request, jsonify # import the request object from the flask module
from app.limiter import limiter # Import the limiter instance from the limiter 
from marshmallow import ValidationError # import the ValidationError class from the marshmallow module
from app.schemas import UserSchema # import the UserSchema class from the schemas module
from flask_oauthlib.provider import OAuth2Provider # import the OAuth2Provider class from the flask_oauthlib.provider module
from app.auth import require_api_key, make_api_key, update_api_key # import the require_api_key function
from flask_limiter import Limiter # Import the limiter instance
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from app.utils import limiter_instance



def return_constant():
    return "constant"

class getRequestV1(Resource): # create a class named getRequestV1 that inherits from the Resource class
    
    oauth = OAuth2Provider()

    #decorators = [limiter.limit("1 per minute")]
  
    print("still working")
    
    #@limiter.limit("1000/minute", key_func=return_constant)
    #@limiter_instance.exempt
    @limiter_instance.limit("5 per minute")

    def get(self): # create a get method
        print("Get method works")
        apiKey = update_api_key()
        return {"message" : f'Hello user, this is version 1, use the key: {apiKey}'} # return the string 'Version1 hello world'
    
    #@limiter.limit("1 per day")
    #decorators = [limiter.limit("10 per minute")]

    @limiter_instance.limit("5 per minute")
    @require_api_key
    def post(self): # create a post method
        print("Post method works")
       # print(limiter.limit("5 per minute"))
        user_schema = UserSchema() # create an instance of the UserSchema class
        
        try: # try block
            json_data = request.get_json() 
            print("here is the statement", type(json_data))
            data = user_schema.load(json_data) # get the JSON data from the request
            
            '''
            missing_fields = set(user_schema.fields.keys) - set(data.keys())
            if missing_fields:
                missing_fields_messages = {field: f'{field.capitalize()} is required' for field in missing_fields}
                return {'message': missing_fields_messages}, 400
            '''

            data_without_sets = {} # create an empty dictionary

            for key, value in data.items(): # iterate over the key-value pairs in the data dictionary
                if (isinstance(value, set)): # check if the value is a set
                    data_without_sets[key] = list(value) # convert the set to a list and add it to the data_without_sets dictionary
                else:
                    data_without_sets[key] = value # add the key-value pair to the data_without_sets dictionary
            
            return {"message": f'Hello {data_without_sets["name"]}! this is version 1, your email is {data_without_sets["email"]}'} # return a formatted string with the name from the JSON data
        
        except ValidationError as err:

            return {"message": 'N/A please input both name and email.'}, 400
        


    


#command to make post request curl -X POST  http://127.0.0.1:5000/v1/hello 
#command to make get request curl -X POST  http://127.0.0.1:5000/v1/hello -H "Content-Type: application/json" -H "x-api-key: [851593]" -d '{"name": "John Doe", "email": "rfernandez@gmail.com"}'
#ngrok http 127.0.0.1:5000
# to update the github repo, here are the commands:
# git add .
# git commit -m "message"
# git push origin main

#curl -X GET https://efd9-2607-fea8-4c26-1800-ec65-8b76-89d-65d3.ngrok-free.app/v1/hello
#curl -X POST https://efd9-2607-fea8-4c26-1800-ec65-8b76-89d-65d3.ngrok-free.app/v1/hello -H "Content-Type: application/json" -H "x-api-key: [387755]" -d '{"name": "Rachel", "email": "rfernandez@gmail.com"}'

# --TASKS--`
# set up to remote server for ehtisham to test
# study versioning in flask restful (done)
# put error handling for throttling (done)
# local (for the user) and the global throttling (for everyone), so every user has a limit of 5 requests per minute, should be able to set between per user or globally, if and else statement (done)
#Change api key after a moment of time ex 2 mins, expired key should give an error? (done)

#make sure configuration where user can access and change rate
#make sure same api key is given even after refresh
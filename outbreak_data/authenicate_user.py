"""
Script to generate authentication token for Python package.

TODO:
    Document everything correctyl with docstring.
    Make sure edge cases are handled properly (ie. what happens if a token isn't returned)
"""

import os 
import sys
import requests



OUTBREAK_INFO_AUTH = "https://api.outbreak.info/genomics/get-auth-token"

def get_authentication():
    """
    Get the authentication token from a 'hidden' file.
    """
    #check for hidden file
    if (auth_token_filename):
        
    #open hidden file 
       with open(auth_token_filename, "r") as A:
          read_token = A.read()
          
    #get token
    token = read_token

    return(token)


def set_authentication(token):
    """
    Set the authentication code by saving it to a 'hidden' file.
    """
    #get the working directory
    curr_dir = os.getcwd() #should try to generalize working directory using paths
    
    #write the authentication token to a file
    global auth_token_filename 
    auth_token_filename = ".Python_outbreak_info_token.txt"
   

    #open file in write mode
    with open(auth_token_filename, "w") as A:
      A.write(token)
   
    #handle the error in which it doesn't write properly
    hidden_file = os.path.join(curr_dir, auth_token_filename)
    if not os.path.isfile(hidden_file):  #check to see if file was saved in directory
        assert (FileNotFoundError)
    get_authentication()
        
        
        

def authenticate_user():
    """
    Authenticate a user for genomics API access.
    """
    ###this code currently doesn't handle a bad request, make sure that the final product does!

    #POST request to the OUTBREAK TOKEN API to get a token 
    r = requests.post(OUTBREAK_INFO_AUTH)
    if (r.status_code != 200):
        print("Could not get authentication-token")
        r.raise_for_status()
        
    #get dat as json
    data = r.json()  #save this json file for program to extract data
    
    #get token from data
    token = data['authn_token']
    
    #get authentication url from response
    auth_url = data['authn_url']

    #ask the user to open the browser and authenticate the url
    print("Please open this url in a web browswer and authenticate with your GISAID credentials: ", auth_url)

    #set authentication token
    set_authentication(token)
    
    #wait until the authorization goes through using a while loop
    import time
    while(True):
        print(f"Waiting for authorization response... [Press Ctrl-C to abort]")
        time.sleep(5)
        
        # response = code authenticates something
        
        
    # if (response.status_code == 200):
    #     print("\nAuthenticated successfully!\n")
    #     # printTerms()
    #     # authToken = response$headers$`x-auth-token`
    #     if(authToken == None):
    #       setAuthToken(authToken)
     
        
    
    
    
#this is just to help you test, delete everything below here in the final version
def main():
    authenticate_user()

if __name__ == "__main__":
    main()

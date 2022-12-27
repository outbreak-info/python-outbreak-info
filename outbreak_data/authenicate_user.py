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
    token = ""
    #check for hidden file

    #open hidden file 

    #get token

    return(token)


def set_authentication(token):
    """
    Set the authentication code by saving it to a 'hidden' file.
    """
    #get the working directory
    
    #write the authentication token to a file
    auth_token_filename = ".Python_outbreak_info_token"

    #open file in write mode


    #handle the error in which it doesn't write properly

def authenticate_user():
    """
    Authenticate a user for genomics API access.
    """

    ###this code currently doesn't handle a bad request, make sure that the final product does!
    token = ""

    #POST request to the OUTBREAK TOKEN API to get a token 

    #get dat as json

    #get token from data

    #get authentication url from response

    #ask the user to open the browser and authenticate the url
    print("Please open this url and authenticate with your GISAID credentials: ", auth_url)

    #set authentication token
    set_authentication(token)
    
    #wait until the authorization for through using a while loop
    
#this is just to help you test, delete everything below here in the final version
def main():
    authenticate_user()

if __name__ == "__main__":
    main()

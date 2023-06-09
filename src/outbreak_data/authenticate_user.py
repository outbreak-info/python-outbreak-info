"""
Script to generate authentication token for Python package.
"""

import os
import sys
import time
import requests
import webbrowser

OUTBREAK_INFO_AUTH = "https://api.outbreak.info/genomics/get-auth-token"
AUTH_TOKEN_FILENAME = os.path.join(os.path.dirname(__file__), "../.Python_outbreak_info_token.txt")

def get_authentication():
    """
    Get the authentication token from a 'hidden' file.
    """
    #check for hidden file
    if os.path.isfile(AUTH_TOKEN_FILENAME): 
        #open hidden file 
        with open(AUTH_TOKEN_FILENAME, "r") as A:
          read_token = A.read()
        if len(read_token) != 0:
           return(read_token)
        else:
            print("No token found, please reauthenticate user.")
            sys.exit(1)

    else:
        print("No token generated, please authenticate user.")
        sys.exit(1)

def set_authentication(token):
    """
    Set the authentication code by saving it to a 'hidden' file.
    """
    #get the working directory
    curr_dir = os.getcwd() #should try to generalize working directory using paths
    
    #open file in write mode
    with open(AUTH_TOKEN_FILENAME, "w") as A:
      A.write(token)
   
    #handle the error in which it doesn't write properly
    hidden_file = os.path.join(curr_dir, AUTH_TOKEN_FILENAME)
    if not os.path.isfile(hidden_file):  #check to see if file was saved in directory
        assert (FileNotFoundError)        
        
def print_terms():
    print("""
    TERMS OF USE for Python Package and
    Reminder of GISAID's Database Access Agreement
    Your ability to access and use Data in GISAID, including your access and
    use of same via R Package, is subject to the terms and conditions of
    GISAID's Database Access Agreement (“DAA”) (which you agreed to
    when you requested access credentials to GISAID), as well as the
    following terms:
    1. You will treat all data contained in the R Package consistent with
    other Data in GISAID and in accordance with GISAID's Database Access
    Agreement;
    2. You will not distribute, or re-distribute Data made available through
    GISAID to any third party other than Authorized Users as contemplated by
    the DAA;
    3. USE OF R PACKAGE: Any visualizations, charts, graphs,
    graphics, pictographs, plots, or other displays you create via the R
    Package may be exclusively used for academic and research purposes.
    No other types of uses are allowed;
    4. Any use of visualizations, charts, graphs, graphics, pictographs,
    plots, or other displays created via the R Package in an academic or
    research publication, including in a paper, manuscript, preprint, website,
    web service, or any other media material must be in conformity with the
    GISAID Publishing Guidelines, available at https://www.gisaid.org/publish,
    and the DAA, available at https://www.gisaid.org/daa; and
    5. By using the R Package you reaffirm your understanding of these
    terms and the DAA.
    When using this data, please state, \"This data was obtained from GISAID via the outbreak.info API\". 
    WE DO NOT SUPPORT THIRD PARTY APPLICATIONS. THIS PACKAGE IS MEANT FOR RESEARCH AND VISUALIZATION PURPOSES ONLY. 
    If you want to build third party applications, please contact GISAID via https://www.gisaid.org/help/contact/.""")

def authenticate_new_user():
    """
    Authenticate a user for genomics API access.
    """
    ###this code currently doesn't handle a bad request, make sure that the final product does!

    #POST request to the OUTBREAK TOKEN API to get a token 
    r = requests.post(OUTBREAK_INFO_AUTH)
    if (r.status_code != 200):
        print("Could not get authentication-token")
        r.raise_for_status()
        
    #get data as json
    data = r.json()  #save this json file for program to extract data
    
    #get token from data
    token = data['authn_token']
    
    #get authentication url from response
    auth_url = data['authn_url']

    #ask the user to open the browser and authenticate the url
    print("Please open this url in a web browswer and authenticate with your GISAID credentials: ", auth_url)
    webbrowser.open(auth_url, new=0, autoraise=True)

    #set authentication token
    set_authentication(token)

    #wait until the authorization goes through using a while loop
    start_time = time.time()
    time.sleep(5) 
    while(True):
        print("Waiting for authorization response... [Press Ctrl-C to abort]")
        
        #get request the OUTBREAK_INFO_AUTH url using the token as header like this: 

        headers = {'Authorization': 'Bearer ' + str(get_authentication())}

        r = requests.get(OUTBREAK_INFO_AUTH, headers=headers)
        #check if the response came through properly
        if (r.status_code == 200):
          print("Authenticated successfully!")
          print_terms()
          
          #parse the header back from the response
          authToken = r.headers['X-Auth-Token']
          if (authToken == None):
              set_authentication(authToken)
          break
      
        else:
            print("Authenication failed, trying again in 5 seconds...")
        time.sleep(5)

        if (time.time() - start_time > 60):
            print("Aborting, please try again.")
            break

from datetime import datetime
import os
import pickle
import re


time_id = datetime.today().strftime('%Y%m%d')


def check_files(dir_files, keyword):
    dict_files = {}

    for file in os.listdir(dir_files):
        key = re.search('^([0-9]+)', file)
        
        if keyword in file and key is not None:
                dict_files[key.group(1)] = file
            
    return dict_files


def last_pickle(dict_pickles):
    last_date = max([date for date in dict_pickles])
    last_pickle = dict_pickles[last_date]

    return last_pickle


def login(username, password, entry_type):
    dir_files = f'{os.getcwd()}\\Credentials'
    dict_pickles = check_files(dir_files, 'credentials')
    
    try:
        selected_pickle = last_pickle(dict_pickles)
        with open(f'{dir_files}\\{selected_pickle}', 'rb') as file:
            credentials = pickle.load(file)
    
    except Exception as e:
        credentials = {}
        
    if entry_type == 'login':
        if (username in list(credentials.keys())) and (password == credentials[username]):
            return 'User successfully logged in!'
        
        elif username not in list(credentials.keys()):
            return 'Username not yet registered.'
        
        elif (username in list(credentials.keys())) and (password != credentials[username]):
            return 'Incorrect password.'
        
    elif entry_type == 'register':
        if username in list(credentials.keys()):
            return 'User already registered.'
        else:
            credentials[username] = password
        
        with open(f'{dir_files}\\{time_id}_credentials_for_ganter_investment.pickle', 'wb') as file:
            pickle.dump(credentials, file)
        
        return 'User successfully registered!'
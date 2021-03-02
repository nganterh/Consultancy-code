from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd
import pickle
import re
import requests
from selenium import webdriver
import time


time_id = datetime.today().strftime('%Y%m%d')
geckodriver_path = r'C:\Users\nicol\anaconda3\Library\bin\geckodriver'


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
    
    
def login_investing(path, username, password):
    investing_url = 'https://www.investing.com/'
    
    browser = webdriver.Firefox(executable_path=geckodriver_path)
    browser.get(investing_url)

    browser.find_element_by_css_selector('.login').click()
    browser.find_element_by_css_selector('#loginFormUser_email').send_keys(username)
    browser.find_element_by_css_selector('#loginForm_password').send_keys(password)
    browser.find_element_by_css_selector('#signup > a:nth-child(4)').click()
    
    return browser


def get_inmutable(browser, country):
    investing_url = 'https://www.investing.com'
    df_main = pd.DataFrame()
    list_urls = []
    
    browser.get(f'{investing_url}/stock-screener/?sp=country::' +
                f'{country}|sector::a|industry::a|equityType::a%3Ceq_market_cap;1')
    
    while True:
        time.sleep(5)

        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')

        soup_table = soup.find('div', {'id':'resultsContainer'})
        html_table = soup_table.prettify()

        urls = [elem.a.get('href') for elem
                in soup_table.find_all('td')
                if (elem.a and elem.a.get('href')) != None]
        
        list_urls.extend(urls)
        list_dfs = pd.read_html(html_table)
        
        for df in list_dfs:
            df_main = df_main.append(df)
            
        try:        
            browser.find_element_by_class_name('blueRightSideArrowPaginationIcon').click()
        except:
            break

    df_main = df_main.reset_index(drop=True)

    columns = [col for col in df_main]
    df_main = df_main.drop([columns[0], columns[-1]], axis=1)
    df_main['url'] = list_urls
    
    return df_main
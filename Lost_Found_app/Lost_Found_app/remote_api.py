import requests
import json 
import os 
from dotenv import load_dotenv

class RemoteAPI:
    def __init__(self):
        load_dotenv()
        self.app_id = os.getenv('APP_ID')
        self.secret = os.getenv('APP_SECRET')

    def create_user(self, name_surname):
        url = 'https://www.saltedge.com/api/v5/customers/'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = json.dumps({'data': {'identifier': name_surname}})
        response = requests.post(url, headers=headers, data=data).json()  
        try:
            response = response["data"]         
            remote_id = response["id"]
            user_secret = response['secret']
            creation_date = response["created_at"] 
        except:
            print(response["error"])
            


    def get_users_list(self):
        url = 'https://www.saltedge.com/api/v5/customers'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        response = requests.get(url, headers=headers).json()  
        print(response)

    def create_user_session(self,usr_id): 
        url = 'https://www.saltedge.com/api/v5/connect_sessions/create'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = json.dumps( {'data': {'customer_id': usr_id,   
                                     
                                     'consent': {'period_days': 90, 'scopes': ['account_details', 'transactions_details']},
                                     
                         'attempt': {'return_to': 'https://example.com/','fetch_scopes': ['accounts', 'transactions']}}})
        response = requests.post(url, headers=headers, data=data).json()   
        try:
            response = response["data"]
            # keep in database temporarily
            expires_at = response["expires_at"]
            connect_url = response["connect_url"]
        except:
            print(response["error"])

    def reconnect_user_session(self, conn_id):
        url = 'https://www.saltedge.com/api/v5/connect_sessions/reconnect'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = json.dumps({'data': {'connection_id': conn_id, 'consent': {'period_days': 90,
                                                                     'scopes': ['account_details']}}})
        response = requests.post(url, headers=headers, data=data).json() 
        # keep in database
        #expires_at = response["expires_at"]

    def refresh_user_session(self, conn_id):
        url = 'https://www.saltedge.com/api/v5/connect_sessions/refresh'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data =  json.dumps({'data': {'connection_id': conn_id, 'attempt': { 
            'return_to': 'https://example.com/', 'fetch_scopes': ['accounts', 'transactions']}}})
        response = requests.post(url, headers=headers, data=data).json()  
        print(response)
        response = response["data"]
        # keep in database
        #expires_at = response["expires_at"]
        #connect_url = response["connect_url"]

    def authentication(self,usr_id):
        url = 'https://www.saltedge.com/api/v5/oauth_providers/create'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = json.dumps(  {'data': {'customer_id': usr_id, 'country_code': 'XF',
                         'provider_code': 'fakebank_oauth_xf', 'consent': {'scopes':
                                                                               ['account_details',
                                                                                'transactions_details']},
                         'attempt': {'return_to': 'https://example.com/',
                                     'fetch_scopes': ['accounts', 'transactions']}, 'return_connection_id': 'true'}} )
        response = requests.post(url, headers=headers, data=data).json()  
        #response = response["data"]
        #token = response["token"]
        #expires_at = response["expires_at"]
        #redirect_url = response["redirect_url"]
        #connection_secret = response["connection_secret"]

    def get_transaction_data(self,conn_id, usr_id):
        url = f'https://www.saltedge.com/api/v5/transactions?connection_id={conn_id}&account_id={usr_id}'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        response = requests.get(url, headers=headers).json() 
        print(response)

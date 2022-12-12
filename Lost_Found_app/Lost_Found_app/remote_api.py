import requests


class RemoteAPI:
    def __init__(self):
        self.app_id = ''
        self.secret = ''

    def create_user(self, name_surname):
        url = 'https://www.saltedge.com/api/v5/customers'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = {'data': {'identifier': name_surname}}
        response = requests.post(url, headers=headers, data=data).json()
        #       the following data should be kept in local database
        remote_id = response["id"]
        user_secret = response['secret']
        creation_date = response["created_at"]

    def get_users_list(self):
        url = 'https://www.saltedge.com/api/v5/customers'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        response = requests.get(url, headers=headers).json()

    def create_user_session(self):
        url = 'https://www.saltedge.com/api/v5/connect_sessions/create'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = {'data': {'customer_id': 'id_from_db', 'consent': {'from_date': 'creation_date_db',
                                                                  'period_days': 90, 'scopes': ['account_details',
                                                                                                'transactions_details']},
                         'attempt': {'from_date': 'current_date', 'fetch_scopes': ['accounts', 'transactions']}}}
        response = requests.post(url, headers=headers, data=data).json()
        # keep in database temporarily
        expires_at = response["expires_at"]
        connect_url = response["connect_url"]

    def reconnect_user_session(self):
        url = 'https://www.saltedge.com/api/v5/connect_sessions/reconnect'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = {'data': {'connection_id': 'get_from_db', 'consent': {'period_days': 90,
                                                                     'scopes': ['account_details']}}}
        response = requests.post(url, headers=headers, data=data).json()
        # keep in database
        expires_at = response["expires_at"]

    def refresh_user_session(self):
        url = 'https://www.saltedge.com/api/v5/connect_sessions/refresh'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = {'data': {'connection_id': 'get_from_db', 'attempt': {'fetch_scopes':
                                                                         ['accounts', 'transactions']}}}
        response = requests.post(url, headers=headers, data=data).json()
        # keep in database
        expires_at = response["expires_at"]
        connect_url = response["connect_url"]

    def authentication(self):
        url = 'https://www.saltedge.com/api/v5/oauth_providers/create'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        data = {'data': {'customer_id': 'get_from_db', 'country_code': 'XF',
                         'provider_code': 'fakebank_oauth_xf', 'consent': {'scopes':
                                                                               ['account_details',
                                                                                'transactions_details'],
                                                                           'from_date': 'creation_date'},
                         'attempt': {'return_to': 'https://example.com/', 'from_date': 'current_date',
                                     'fetch_scopes': ['accounts', 'transactions']}, 'return_connection_id': 'false'}}
        response = requests.post(url, headers=headers, data=data).json()
        token = response["token"]
        expires_at = response["expires_at"]
        redirect_url = response["redirect_url"]
        connection_secret = response["connection_secret"]

    def get_transaction_data(self):
        url = f'https://www.saltedge.com/api/v5/transactions?connection_id={"connection.id"}&account_id={"account.id"}'
        headers = {'Accept': 'application/json', 'Content-type': 'application/json',
                   'App-id': self.app_id, 'Secret': self.secret}
        response = requests.get(url, headers=headers).json()

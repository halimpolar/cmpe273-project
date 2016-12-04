from __future__ import print_function
import json
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build


class OrderHandler:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'Alexa_Pizza.json', scopes)
        http_auth = credentials.authorize(Http())
        self.service = build('sheets', 'v4', http=http_auth)
        self.sheetID = '1rJ6-8LPsQJFXMeQVC-RfruSuF5IQO57Oujvl2FHjgR8'
        self.sheetName = 'SimpleOrder'

    def placeOrder(self, order):
        rangeName = self.sheetName + '!B3:F'
        values = [
            [
                # order['name'], order['type'], order['size'], order['crusts'], order['toppings']
                order['name'], order['type'], order['size'], '', '', order['bake']
            ]
        ]
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheetID, range=rangeName,
                valueInputOption='RAW', body=body).execute()


if __name__ == '__main__':
    test = OrderHandler()
    test.placeOrder(None)

from __future__ import print_function
import json
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build


class MenuHandler:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'Alexa_Pizza.json', scopes)
        http_auth = credentials.authorize(Http())
        self.service = build('sheets', 'v4', http=http_auth)
        self.sheetID = '1rJ6-8LPsQJFXMeQVC-RfruSuF5IQO57Oujvl2FHjgR8'
        self.sheetName = 'ActualMenu'

    def getPizzaTypes(self):
        rangeName = self.sheetName + '!O2:O'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaSizes(self):
        rangeName = self.sheetName + '!C2:C'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaCrusts(self):
        rangeName = self.sheetName + '!A2:A'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaToppings(self):
        rangeName = self.sheetName + '!M3:M'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaBakes(self):
        rangeName = self.sheetName + '!G2:G'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaCuts(self):
        rangeName = self.sheetName + '!I2:I'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaSauces(self):
        rangeName = self.sheetName + '!E2:E'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values


if __name__ == '__main__':
    menuHandler = MenuHandler()

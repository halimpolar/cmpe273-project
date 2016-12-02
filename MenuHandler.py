from __future__ import print_function
from apiclient.discovery import build


ORDER = {
    'type': None,
    'size': None,
    'crusts': None,
    'toppings': None
}


class MenuHandler:
    def __init__(self):
        self.sheetID = '1rJ6-8LPsQJFXMeQVC-RfruSuF5IQO57Oujvl2FHjgR8'
        self.sheetName = 'Menu'
        self.service = build('sheets', 'v4', developerKey='AIzaSyCkiKIX1pHyXVZrm5lkuALr9P7cqLwDPW8')

    def getPizzaTypes(self):
        rangeName = self.sheetName + '!A2:A'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaSizes(self):
        rangeName = self.sheetName + '!B2:B'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaCrusts(self):
        rangeName = self.sheetName + '!C2:C'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    def getPizzaToppings(self):
        rangeName = self.sheetName + '!D2:D'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values

    # check the information we want before writting to sheet
    def hasEnoughInfo(self):
        global ORDER
        for key in ORDER.keys():
            if ORDER[key] is None:
                return False, key
        return True

    def writeData(self, key, value):
        global ORDER
        ORDER[key] = value

if __name__ == '__main__':
    menuHandler = MenuHandler()
    print(menuHandler.hasEnoughInfo())
    menuHandler.writeData('type', 'hello')
    print(menuHandler.hasEnoughInfo())
    toppings = ['1', '2']
    menuHandler.writeData('toppings', toppings)
    print(menuHandler.hasEnoughInfo())
    menuHandler.writeData('size', 'hello2')
    print(menuHandler.hasEnoughInfo())
    crusts = ['1', '2']
    menuHandler.writeData('crusts', crusts)
    print(menuHandler.hasEnoughInfo())
    '''
    types = menuHandler.getPizzaType()
    print('Types: ')
    for pizza in types:
        print("{}".format(pizza[0]))
    print('Sizes: ')
    for size in menuHandler.getPizzaSize():
        print("{}".format(size[0]))
    '''

from __future__ import print_function
from apiclient.discovery import build


class MenuHandler:
    def __init__(self):
        self.sheetID = '1rJ6-8LPsQJFXMeQVC-RfruSuF5IQO57Oujvl2FHjgR8'
        self.sheetName = 'Menu'
        self.service = build('sheets', 'v4', developerKey='AIzaSyCkiKIX1pHyXVZrm5lkuALr9P7cqLwDPW8')

    def getMenu(self):
        rangeName = self.sheetName + '!A2:A'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return values


if __name__ == '__main__':
    menuHandler = MenuHandler()
    menu = menuHandler.getMenu()
    for pizza in menu:
        print("{}".format(pizza[0]))
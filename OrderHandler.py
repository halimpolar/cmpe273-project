from __future__ import print_function
import json
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
import time


class OrderHandler:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'Alexa_Pizza.json', scopes)
        http_auth = credentials.authorize(Http())
        self.service = build('sheets', 'v4', http=http_auth)
        self.sheetID = '1rJ6-8LPsQJFXMeQVC-RfruSuF5IQO57Oujvl2FHjgR8'
        self.sheetName = 'Order'

    def getExistingOrders(self):
        rangeName = self.sheetName + '!A2:AC'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return len(values)

    def getTotalPriceOfNewOrder(self, rangeName):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return str(values[0][27])

    def getOrderNumbers(self, sheets=''):
        values = []
        if sheets == '':
            rangeName = self.sheetName + '!B2:B'
        else:
            rangeName = self.sheetName + sheets
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values')
        return (values)

    def getPersonOrder(self, name):
        values = []
        rangeName = self.sheetName + '!A2:B'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        for x in result.get('values'):
            if x[0] == name:
                values.append(int(x[1]))
        return (values)

    def getCustomerInfos(self):
        rangeName = 'Member' + '!A2:C'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        members = []
        for value in values:
            member = {
                'ID': value[0],
                'Name': value[1],
                'Awards': value[2]
            }
            members.append(member)
        return members

    def getExistingMembers(self):
        rangeName = 'Member' + '!A2:C'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheetID, range=rangeName).execute()
        values = result.get('values', [])
        return len(values)

    def updateMemberAwards(self, member):
        row = int(member['ID']) + 1
        rangeName = 'Member!A' + str(row) + ':C'
        values = [
            [
                int(member['ID']),
                member['Name'],
                member['Awards']
            ]
        ]
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheetID, range=rangeName,
                valueInputOption='RAW', body=body).execute()

    def createNewMember(self, name, no_of_pizza):
        new_member_no = self.getExistingMembers() + 1
        rangeName = 'Member!A2:C'
        values = [
            [
                new_member_no,
                name,
                no_of_pizza
            ]
        ]
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheetID, range=rangeName,
                valueInputOption='RAW', body=body).execute()
        return new_member_no

    def placeOrder(self, order, member):
        # before appending a new row of order,
        # we should fetch the existing data,
        # to get the next order_no
        existing_rows = self.getExistingOrders()
        new_row_num = str(existing_rows + 2)
        new_order_no = str(existing_rows + 1)

        # default total
        total = '=C'+new_row_num+'*(E'+str(new_row_num)+'+G'+str(new_row_num)+'+I'+str(new_row_num)+'+K'+str(new_row_num)+'+M'+str(new_row_num)+'+O'+str(new_row_num)+'+Q'+str(new_row_num)+'+S'+str(new_row_num)+'+U'+str(new_row_num)+'+W'+str(new_row_num)+'+Y'+str(new_row_num)+'+AA'+str(new_row_num)+')'

        # when user is our member, we should update the member awards and redeem
        awards = None
        redeemCount = 0
        if member is not None:
            awards = int(member['Awards']) + int(order['no_of_pizza'])
            if awards > 10:
                redeemCount = awards / 10
                awards = awards % 10 - 1
                after_redeem_count = int(order['no_of_pizza']) - redeemCount
                total = '='+str(after_redeem_count)+'*(E'+str(new_row_num)+'+G'+str(new_row_num)+'+I'+str(new_row_num)+'+K'+str(new_row_num)+'+M'+str(new_row_num)+'+O'+str(new_row_num)+'+Q'+str(new_row_num)+'+S'+str(new_row_num)+'+U'+str(new_row_num)+'+W'+str(new_row_num)+'+Y'+str(new_row_num)+'+AA'+str(new_row_num)+')'
            # update the awards of member
            member['Awards'] = awards
            self.updateMemberAwards(member)

        rangeName = self.sheetName + '!A' + new_row_num + ':AA'
        values = [
            [
                # name
                order['name'],
                # order_no
                new_order_no,
                # no_of_pizza
                order['no_of_pizza'],
                # pizza_type
                order['type'],
                # pizza price
                '=vlookup(D' + new_row_num + ',ActualMenu!$O$2:$P,2,false)',
                # pizza size
                order['size'],
                # pizza size price
                '=vlookup(F' + new_row_num + ',ActualMenu!$C$2:$D,2,false)',
                # pizza crust
                order['crust'],
                # pizza crusts price
                '=vlookup(H' + new_row_num + ',ActualMenu!$A$2:$B,2,false)',
                # pizza sauce
                order['sauce'],
                # pizza sauce price
                '=vlookup(J' + new_row_num + ',ActualMenu!$E$2:$F,2,false)',
                # pizza bake
                order['bake'],
                # pizza bake price
                '=vlookup(L' + new_row_num + ',ActualMenu!$G$2:$H,2,false)',
                # pizza cut
                order['cut'],
                # pizza cut price
                '=vlookup(N' + new_row_num + ',ActualMenu!$I$2:$J,2,false)',
                # pizza seasoning
                order['seasoning'],
                # pizza seasoning price
                '=vlookup(P' + new_row_num + ',ActualMenu!$K$2:$L,2,false)',
                # pizza topping-1
                order['toppings'][0],
                # pizza topping-1 price
                '=vlookup(R' + new_row_num + ',ActualMenu!$M$2:$N,2,false)',
                # pizza topping-2
                order['toppings'][1],
                # pizza topping-2 price
                '=vlookup(T' + new_row_num + ',ActualMenu!$M$2:$N,2,false)',
                # pizza topping-3
                order['toppings'][2],
                # pizza topping-3 price
                '=vlookup(V' + new_row_num + ',ActualMenu!$M$2:$N,2,false)',
                # pizza topping-4
                order['toppings'][3],
                # pizza topping-4 price
                '=vlookup(X' + new_row_num + ',ActualMenu!$M$2:$N,2,false)',
                # pizza topping-5
                order['toppings'][4],
                # pizza topping-5 price
                '=vlookup(Z' + new_row_num + ',ActualMenu!$M$2:$N,2,false)',
                # total
                total,
                # timestamp
                time.time()
            ]
        ]
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheetID, range=rangeName,
                valueInputOption='USER_ENTERED', body=body).execute()

        # after placing a new order, return the order_no and total price to user
        # fetch the total price
        rangeName = self.sheetName + '!A' + new_row_num + ':AC' + new_row_num

        return str(new_order_no), self.getTotalPriceOfNewOrder(rangeName), awards, redeemCount

if __name__ == '__main__':
    test = OrderHandler()
    test.placeOrder(None)

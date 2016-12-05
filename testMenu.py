from MenuHandler import MenuHandler
from collections import OrderedDict


# ORDER = OrderedDict()
ORDER = {}
ORDER['type'] = None
ORDER['size'] = None
ORDER['crusts'] = None
ORDER['toppings'] = None


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


def printOrder():
    global ORDER
    for key in ORDER.keys():
        print(key)

if __name__ == '__main__':
    printOrder()
    '''
    menuHandler = MenuHandler()
    menu = menuHandler.getMenu()
    print("{} in {} costs {}".format(menu[0][0], menu[0][1], menu[0][2]))
    '''
    '''
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

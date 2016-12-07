from ask import alexa
from MenuHandler import MenuHandler
from OrderHandler import OrderHandler
from collections import OrderedDict

HasLoaded = False
PIZZAS = []
SIZES = []
CRUSTS = []
BAKES = []
SAUCES = []
CUTS = []
SEASONINGS = []
TOPPINGS = []
ORDER = OrderedDict()
ORDER['member'] = None
ORDER['name'] = None
ORDER['type'] = None
ORDER['size'] = None
ORDER['crust'] = None
ORDER['sauce'] = None
ORDER['bake'] = None
ORDER['cut'] = None
ORDER['seasoning'] = None
ORDER['toppings'] = None
ORDER['no_of_pizza'] = None
ORDER['ask_enroll'] = None


def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''
    # add your own metadata to the request using key value pairs
    metadata = {'user_name': 'SomeUserName'}
    ''' inject user relevant metadata into the request if you want to, here.
    e.g. Something like :
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}
    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''

    '''
    Tring to load pizza menus in to global variables
    '''
    global HasLoaded
    if not HasLoaded:
        menuHandler = MenuHandler()
        # pizza types
        global PIZZAS
        for pizza in menuHandler.getPizzaTypes():
            PIZZAS.append(pizza[0].lower())
        # pizza sizes
        global SIZES
        for size in menuHandler.getPizzaSizes():
            SIZES.append(size[0].lower())
        # pizza crusts
        global CRUSTS
        for crust in menuHandler.getPizzaCrusts():
            CRUSTS.append(crust[0].lower())
        # pizza bakes
        global BAKES
        for bake in menuHandler.getPizzaBakes():
            BAKES.append(bake[0].lower())
        # pizza sauces
        global SAUCES
        for s in menuHandler.getPizzaSauces():
            SAUCES.append(s[0].lower())
        # pizza cuts
        global CUTS
        for c in menuHandler.getPizzaCuts():
            CUTS.append(c[0].lower())
        # pizza toppings
        global TOPPINGS
        for topping in menuHandler.getPizzaToppings():
            TOPPINGS.append(topping[0].lower())
        # pizza seasonings
        global SEASONINGS
        for topping in menuHandler.getPizzaSeasonings():
            SEASONINGS.append(topping[0].lower())

        # set flag to true
        HasLoaded = True

    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    reply = 'Hello, '
    global ORDER
    if ORDER['name'] is not None:
        reply += ORDER['name'] + '. '
    reply += 'Welcome to the Pizza Ordering System. '
    reply += checkIsReady()
    return alexa.create_response(message=reply, end_session=False)


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent_handler("EnrollForAwards")
def launch_AskForEnroll_handler(request):
    global ORDER
    ORDER['ask_enroll'] = True
    orderHandler = OrderHandler()
    new_member_no = orderHandler.createNewMember(ORDER['name'], ORDER['no_of_pizza'])
    ORDER['member'] = {
        'ID': new_member_no,
        'Name': ORDER['name'],
        'Awards': 0
    }
    reply = 'Great, you member ID is: ' + str(new_member_no) + '. '
    r, card = checkIsReady()
    reply += r
    return alexa.create_response(message=reply, end_session=False, card_obj=card)


@alexa.intent_handler("NotEnrollForAwards")
def launch_AskForEnroll_handler(request):
    global ORDER
    ORDER['ask_enroll'] = False
    reply = "Ok, no problem! "
    r, card = checkIsReady()
    reply += r
    return alexa.create_response(message=reply, end_session=False, card_obj=card)


@alexa.intent_handler("IsNotMember")
def launch_IsNotMember_handler(request):
    orderHandler = OrderHandler()
    global ORDER
    ORDER['member'] = {}
    reply = "it's fine! You can join later. "
    reply += checkIsReady()
    return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler("IsMember")
def launch_IsMember_handler(request):
    customer_id = request.slots["customer_id"]
    orderHandler = OrderHandler()
    global ORDER
    ORDER['member'] = {}
    for member in orderHandler.getCustomerInfos():
        if int(customer_id) is int(member['ID']):
            ORDER['member'] = member
            ORDER['ask_enroll'] = True
            ORDER['name'] = member['Name']

    if ORDER['member'] != {}:
        reply = "Hi {}, welcome back. ".format(ORDER['name'])
    else:
        reply = "Sorry, We don't have your information in our database. "
    reply += checkIsReady()
    return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler("AskName")
def launch_AskName_handler(request):
    # global menuHandler
    name = request.slots["name"]

    reply = "Hi {}. ".format(name)
    # write name into Order
    global ORDER
    ORDER['name'] = name
    reply += checkIsReady()
    return alexa.create_response(message=reply, end_session=False)


''' Showing '''
@alexa.intent_handler("ShowPizzaTypes")
def launch_ShowPizzaTypes_handler(request):
    r = "pizza types are "
    global PIZZAS
    for x in PIZZAS:
        r = r + '{},'.format(x)
    card = alexa.create_card(title="Pizza Menu", subtitle=None, content=r)
    return alexa.create_response(message=r, end_session=False, card_obj=card)
    '''
    global PIZZAS
    return alexa.create_response(message="pizza types: {}, {}".format(PIZZAS[0], PIZZAS[1]))
    '''


@alexa.intent_handler("ShowPizzaCrusts")
def launch_ShowPizzaCrusts_handler(request):
    r = "crusts type are "
    global CRUSTS
    for x in CRUSTS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r, end_session=False)


@alexa.intent_handler("ShowPizzaToppings")
def launch_ShowPizzaToppings_handler(request):
    r = "pizza toppings are "
    global TOPPINGS
    for x in TOPPINGS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r, end_session=False)


@alexa.intent_handler("ShowPizzaSizes")
def launch_ShowPizzaSizes_handler(request):
    r = "pizza sizes are "
    global SIZES
    for x in SIZES:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r, end_session=False)


@alexa.intent_handler("ShowPizzaSauces")
def launch_ShowSaucesTypes_handler(request):
    r = "sauces types are "
    global SAUCES
    for x in SAUCES:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r, end_session=False)


@alexa.intent_handler("ShowPizzaCuts")
def launch_ShowCutsTypes_handler(request):
    r = "cuts types are "
    global CUTS
    for x in CUTS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r, end_session=False)


@alexa.intent_handler("ShowPizzaBakes")
def launch_ShowBakes_handler(request):
    r = "baked options are "
    global BAKES
    for x in BAKES:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r, end_session=False)


@alexa.intent_handler("OrderStatus")
def launch_OrderStatus_handler(request):
    o = int(request.slots["order"])
    orderHandler = OrderHandler()
    existing_order = []
    for e in orderHandler.getOrderNumbers():
        existing_order.append(e[0])

    if str(o) in existing_order:
        temp = o+1
        sheet = '!AC'+str(temp)+':AC'+str(temp)
        values = int(((orderHandler.getOrderNumbers(sheet))[0])[0])

        import time
        if (values + 15*60) > time.time():
            min = round(int((((values + 15*60) - time.time())/60)))
            reply = 'Your order will be ready in roughly ' + str(min)[0:2] + ' minutes'
        else:
            reply = 'Your order is ready! Go grab it.'

    else:
        reply = 'Im sorry I dont have that order'
    return alexa.create_response(message=reply, end_session=False)
''' Showing '''


''' Choosing '''
@alexa.intent_handler('ChoosePizzaTypes')
def get_pizza_type_handler(request):
    pizza = request.slots["pizza"].lower()
    global PIZZAS
    if pizza in PIZZAS:
        reply = 'OK, order ' + pizza + '. '
        # save type into order
        global ORDER
        ORDER['type'] = pizza
        reply += checkIsReady()
        return alexa.create_response(message=reply, end_session=False)
    else:
        reply = "I could not find it. says 'show pizza types' to see your options"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler('ChoosePizzaSizes')
def get_pizza_size_handler(request):
    size = request.slots["size"].lower()
    global SIZES
    if size in SIZES:
        reply = "Ok, you pick " + size + " size. "
        # save size into order
        global ORDER
        ORDER['size'] = size
        reply += checkIsReady()
        return alexa.create_response(message=reply, end_session=False)
    else:
        reply = "I could not get it. says 'show pizza sizes' to see your options"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler('ChoosePizzaCrusts')
def get_pizza_crust_handler(request):
    crust = request.slots["crust"].lower()
    reply = "your crust will be " + crust + ". "
    global CRUSTS
    if crust in CRUSTS:
        reply = "Ok, pizza crust will be " + crust + ". "
        # save crust into order
        global ORDER
        ORDER['crust'] = crust
        reply += checkIsReady()
        return alexa.create_response(message=reply, end_session=False)
    else:
        reply = "I could not find it. says 'show pizza crusts' to see your options"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler('ChoosePizzaBakes')
def launch_ChoosePizzaBake_handler(request):
    bake = request.slots["bake"].lower()
    reply = "you want your pizza to be baked in " + bake + ". "
    global BAKES
    if bake in BAKES:
        reply = "Ok, pizza will be baked in " + bake + ". "
        # save bake into order
        global ORDER
        ORDER['bake'] = bake
        reply += checkIsReady()
        return alexa.create_response(message=reply, end_session=False)
    else:
        reply = "I could not find it, if you want me to read menu, say 'show pizza bakes'"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler('AMAZON.StartOverIntent')
def launch_AMAZON_StartOverIntent_handler(request):
    initialzeOrder()
    reply = "Ok, start over!! "
    reply += checkIsReady()
    return alexa.create_response(message=reply)


@alexa.intent_handler("ReOrder")
def launch_ReOrder_handler(request):
    oid = int(request.slots["orderid"])
    global ORDER
    name = ORDER['name']
    orderHandler = OrderHandler()
    orders = orderHandler.getPersonOrder(name)
    if oid in orders:
        temp = oid+1
        sheet = '!C'+str(temp)+':Z'
        get_order = orderHandler.getOrderNumbers(sheet)[0]
        # ORDER = OrderedDict()
        ORDER['name'] = name
        ORDER['type'] = get_order[1]
        ORDER['size'] = get_order[3]
        ORDER['crust'] = get_order[5]
        ORDER['sauce'] = get_order[7]
        ORDER['bake'] = get_order[9]
        ORDER['cut'] = get_order[11]
        ORDER['seasoning'] = get_order[13]
        ORDER['toppings'] = [get_order[15], get_order[17], get_order[19], get_order[21], get_order[23]]
        ORDER['no_of_pizza'] = get_order[0]
        reply, card = checkIsReady()
        return alexa.create_response(message=reply, end_session=False, card_obj=card)
    else:
        return alexa.create_response(message='I am sorry i dont find that order in your name. Please try again.')


@alexa.intent_handler('ChooseSauceTypes')
def get_sauce_type_handler(request):
    sauce = request.slots["sauce"].lower()
    global SAUCES
    if sauce in SAUCES:
        reply = 'OK, ' + sauce + ' sauce. '
        # save type into order
        global ORDER
        ORDER['sauce'] = sauce
        reply += checkIsReady()
        return alexa.create_response(message=reply, end_session=False)
    else:
        reply = "I could not find it. says 'show pizza sauces' to see your options"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler('ChooseCutTypes')
def get_cut_type_handler(request):
    cut = request.slots["cut"].lower()
    global CUTS
    if cut in CUTS:
        reply = 'OK, ' + cut + ' cut. '
        # save type into order
        global ORDER
        ORDER['cut'] = cut
        reply += checkIsReady()
        return alexa.create_response(message=reply, end_session=False)
    else:
        reply = "I could not find it. says 'show pizza cuts' to see your options"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler("numberoforder")
def launch_number_handler(request):
    global ORDER
    num = int(request.slots["num"])
    if num >= 1:
        reply = "ordering {} pizzas. ".format(num)
        ORDER['no_of_pizza'] = num
        r, card = checkIsReady()
        reply += r
        return alexa.create_response(message=reply, card_obj=card)
    else:
        reply = "I could not get it, please say the number of pizza you want"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler("ChoosePizzaToppings")
def get_toppings_handler(request):
    input_topping = request.slots["topping"].lower()
    global TOPPINGS
    if input_topping in TOPPINGS:
        reply = 'OK, add ' + input_topping + '. '
        # save type into order
        global ORDER
        '''
        if ORDER['toppings'] is None:
            ORDER['toppings'] = []
        '''
        ORDER['toppings'].append(input_topping)
        '''
        if len(ORDER['toppings']) < 5:
            ORDER['toppings'].append(input_topping)
        else:
            return alexa.create_response(message='Sorry, you can only choose 5 toppings! ')
        '''
        reply += checkIsReady()
        return alexa.create_response(message=reply, end_session=False)
    else:
        reply = "I could not find it. says 'show pizza toppings' to see your options"
        return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler("StopChoosingToppings")
def launch_StopChoosingToppings_handler(request):
    r = ''
    global ORDER
    if len(ORDER['toppings']) is 0:
        r += "OK, you don't want any topping. "
    else:
        r += 'Ok, you already chose ' + str(len(ORDER['toppings'])) + ' toppings. '
    count = 5 - len(ORDER['toppings'])
    for x in range(0, count):
        ORDER['toppings'].append('none')
    r += checkIsReady()
    return alexa.create_response(message=r, end_session=False)


@alexa.intent_handler("AMAZON.YesIntent")
def get_seasonings_handler(request):
    reply = 'Ok, you want garlic seasoned crust. '
    global ORDER
    ORDER['seasoning'] = 'Garlic Seasoned Crust'
    reply += checkIsReady()
    return alexa.create_response(message=reply, end_session=False)


@alexa.intent_handler("AMAZON.NoIntent")
def get_seasonings_handler(request):
    reply = 'Ok, you do not want any seasoning. '
    global ORDER
    ORDER['seasoning'] = 'none'
    reply += checkIsReady()
    return alexa.create_response(message=reply, end_session=False)
''' Choosing '''


# check the order and reply to user
def checkIsReady():
    isReady, key = hasEnoughInfo()
    if isReady:
        order_no, total_price, awards, redeemCount = placeOrder()
        reply = 'Thank you! Your order number is ' + order_no + '. '
        reply += 'And the total will be $' + total_price + '. '
        reply += 'Your pizza will be ready in 15 minutes. '
        if redeemCount > 0:
            reply += 'Congratulations, you have ' + str(redeemCount) + ' free pizza in this order. '
        if awards is not None:
            difference_awards = 10 - int(awards)
            reply += 'Order ' + str(difference_awards) + " more pizzas, and you will get one free. "
        # return complete info to user for the order
        global ORDER
        content = 'Order Number: ' + order_no + '\n'
        content += 'Customer Name: ' + ORDER['name'] + '\n'
        content += 'Pizza Type: ' + ORDER['type'] + '\n'
        content += 'Pizza Size: ' + ORDER['size'] + '\n'
        content += 'Pizza Crust: ' + ORDER['crust'] + '\n'
        content += 'Pizza Sauce: ' + ORDER['sauce'] + '\n'
        content += 'Pizza Bake: ' + ORDER['bake'] + '\n'
        content += 'Pizza Cut: ' + ORDER['cut'] + '\n'
        content += 'Pizza Seasoning: ' + ORDER['seasoning'] + '\n'
        content += 'Pizza Toppings: '
        count = 1
        for topping in ORDER['toppings']:
            if topping is not 'none':
                content += str(count) + '. ' + topping + ' '
                count += 1
        content += '\n'
        content += 'Number of Pizza: ' + str(ORDER['no_of_pizza']) + '\n'
        content += 'Total Price: $' + total_price + '\n'
        card = alexa.create_card(title="Pizza Order Detail", subtitle=None, content=content)
        initialzeOrder()
        return reply, card
    else:
        if key is 'member':
            return 'Are you in our membership? '
        elif key is 'name':
            return 'Please tell me your name. '
        elif key is 'type':
            return 'Please choose a type of pizza. '
        elif key is 'size':
            return 'Please choose the size for the pizza. '
        elif key is 'crust':
            return 'Please choose the crust for the pizza. '
        elif key is 'sauce':
            return 'Please choose the sauce for the pizza. '
        elif key is 'bake':
            return 'How would you like your pizza to bake, well done or normal? '
        elif key is 'cut':
            return 'Please choose the cut for the pizza. '
        elif key is 'seasoning':
            return 'Do you want garlic seasoned crust for the seasoning? '
        elif key is 'toppings':
            return 'Do you want any topping? You can choose 5 toppings if you want. '
        elif key is 'more_toppings':
            return 'Any other toppings? '
        elif key is 'no_of_pizza':
            return 'How many pizza do you want? '
        elif key is 'ask_enroll':
            return 'Do you want to join our awards program? ', None


# check the information we want before writting to sheet
def hasEnoughInfo():
    global ORDER
    for key in ORDER.keys():
        if key is 'toppings':
            if ORDER[key] is None:
                ORDER[key] = []
                return False, key
            else:
                if len(ORDER[key]) < 5:
                    return False, 'more_toppings'
        else:
            if ORDER[key] is None:
                return False, key

    return True, None


# after we get all the information, write order to the sheet
def placeOrder():
    orderHandler = OrderHandler()
    global ORDER
    if ORDER['member'] != {}:
        return orderHandler.placeOrder(ORDER, ORDER['member'])
    return orderHandler.placeOrder(ORDER, None)


# after ordering
def initialzeOrder():
    global ORDER
    ORDER = OrderedDict()
    ORDER['member'] = None
    ORDER['name'] = None
    ORDER['type'] = None
    ORDER['size'] = None
    ORDER['crust'] = None
    ORDER['sauce'] = None
    ORDER['bake'] = None
    ORDER['cut'] = None
    ORDER['seasoning'] = None
    ORDER['toppings'] = None
    ORDER['no_of_pizza'] = None
    ORDER['ask_enroll'] = None

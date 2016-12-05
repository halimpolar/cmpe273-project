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
TOPPINGS = []
SEASONINGS = []
ORDER = OrderedDict()
ORDER['name'] = None
ORDER['type'] = None
ORDER['size'] = None
ORDER['crust'] = 'handmade'
ORDER['sauce'] = 'barbeque'
ORDER['bake'] = 'well done'
ORDER['cut'] = 'pie'
ORDER['seasoning'] = 'garlic seasoned crust'
ORDER['toppings'] = ['bacon', 'none', 'none', 'none', 'none']
ORDER['no_of_pizza'] = None


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
            SAUCES.append(s[0])
        # pizza cuts
        global CUTS
        for c in menuHandler.getPizzaCuts():
            CUTS.append(c[0])
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
    return alexa.create_response(message="Hello! Welcome to the Pizza Ordering System")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent_handler("AskName")
def launch_AskName_handler(request):
    # global menuHandler
    name = request.slots["name"]

    reply = "Hi {}. ".format(name)
    # write name into Order
    global ORDER
    ORDER['name'] = name
    reply += checkIsReady()
    return alexa.create_response(message=reply)


''' Showing '''
@alexa.intent_handler("ShowPizzaTypes")
def launch_ShowPizzaTypes_handler(request):
    r = "pizza toppings are "
    global PIZZAS
    for x in PIZZAS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)

@alexa.intent_handler("ShowPizzaCrusts")
def launch_ShowPizzaCrusts_handler(request):
    r = "pizza toppings are "
    global CRUSTS
    for x in CRUSTS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)

@alexa.intent_handler("ShowPizzaToppings")
def launch_ShowPizzaToppings_handler(request):
    r = "pizza toppings are "
    global TOPPINGS
    for x in TOPPINGS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)

@alexa.intent_handler("ShowPizzaSizes")
def launch_ShowPizzaSizes_handler(request):
    r = "pizza sizes are "
    global SIZES
    for x in SIZES:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)

@alexa.intent_handler("ShowPizzaSauces")
def launch_ShowSaucesTypes_handler(request):
    r = "sauces types are "
    global SAUCES
    for x in SAUCES:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)


@alexa.intent_handler("ShowPizzaCuts")
def launch_ShowCutsTypes_handler(request):
    r = "cuts types are "
    global CUTS
    for x in CUTS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)
    
@alexa.intent_handler("ShowPizzaSeasonings")
def launch_ShowSeasoningsTypes_handler(request):
    r = "Seasonings are "
    global SEASONINGS
    for x in SEASONINGS:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)
    
@alexa.intent_handler("ShowPizzaBakes")
def launch_ShowBakes_handler(request):
    r = "bake options are "
    global BAKES
    for x in BAKES:
        r = r + '{},'.format(x)
    return alexa.create_response(message=r)  
''' Showing '''


''' Choosing '''
@alexa.intent_handler('ChoosePizzaTypes')
def get_pizza_type_handler(request):
    pizza = request.slots["pizza"].lower()
    reply = 'you ordered ' + pizza + '. '
    global PIZZAS
    if pizza in PIZZAS:
        reply = 'OK, order ' + pizza + '.'
        # save type into order
        global ORDER
        ORDER['type'] = pizza
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, if you want me to read menu, say 'show pizza types'"
        return alexa.create_response(message=reply)


@alexa.intent_handler('ChoosePizzaSizes')
def get_pizza_size_handler(request):
    size = request.slots["size"]
    global SIZES
    if size in SIZES:
        reply = "Ok, ordering pizza in size of " + size + ". "
        # save size into order
        global ORDER
        ORDER['size'] = size
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not get it, if you want me to read the pizza size, say 'show pizza sizes'"
        return alexa.create_response(message=reply)


@alexa.intent_handler('ChoosePizzaCrusts')
def get_pizza_crust_handler(request):
    crust = request.slots["crust"]
    reply = "your crust will be " + crust + ". "
    global CRUSTS
    if crust in CRUSTS:
        reply = "Ok, pizza crust will be " + crust + ". "
        # save crust into order
        global ORDER
        ORDER['crust'] = crust
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, if you want me to read the crust choices, say show pizza crusts"
        return alexa.create_response(message=reply)


@alexa.intent_handler('ChoosePizzaBakes')
def launch_ChoosePizzaBake_handler(request):
    bake = request.slots["bake"]
    reply = "you want your pizza to be baked in " + bake + ". "
    global BAKES
    if bake in BAKES:
        reply = "Ok, pizza will be baked in " + bake + ". "
        # save bake into order
        global ORDER
        ORDER['bake'] = bake
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, if you want me to read menu, say 'show pizza bakes'"
        return alexa.create_response(message=reply)


@alexa.intent_handler('ChooseSauceTypes')
def get_sauce_type_handler(request):
    sauce = request.slots["sauce"]
    reply = 'you ordered ' + sauce + '. '
    global SAUCES
    if sauce in SAUCES:
        reply = 'OK, order ' + sauce + '. '
        # save type into order
        global ORDER
        ORDER['sauce'] = sauce
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, if you want me to read menu, say 'show pizza sauces'"
        return alexa.create_response(message=reply)


@alexa.intent_handler('ChooseCutTypes')
def get_cut_type_handler(request):
    cut = request.slots["cut"]

    reply = 'you ordered ' + cut + '. '
    global CUTS
    if cut in CUTS:
        reply = 'OK, order ' + cut + '. '
        # save type into order
        global ORDER
        ORDER['cut'] = cut
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, if you want me to read menu, say 'show pizza cuts'"
        return alexa.create_response(message=reply)


@alexa.intent_handler("numberoforder")
def launch_number_handler(request):
    global ORDER
    num = request.slots["num"]
    if num >= 1:
        reply = "ordering {} pizzas".format(num)
        ORDER['no_of_pizza'] = num
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, please say it again"
        return alexa.create_response(message=reply)
        
@alexa.intent_handler("ChoosePizzaToppings")
def get_toppings_handler(request):
    topping = request.slots["topping"]

    reply = 'you ordered ' + topping + '. '
    global TOPPINGS
    if topping in TOPPINGS:
        reply = 'OK, order ' + topping + '. '
        # save type into order
        global ORDER
        ORDER['topping'] = topping
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, if you want me to read menu, say 'show pizza toppings'"
        return alexa.create_response(message=reply)
        
@alexa.intent_handler("ChoosePizzaSeasonings")
def get_seasonings_handler(request):
    seasoning = request.slots["seasoning"]

    reply = 'you ordered ' + seasoning + '. '
    global SEASONINGS
    if seasoning in SEASONINGS:
        reply = 'OK, order ' + seasoning + '. '
        # save type into order
        global ORDER
        ORDER['seasoning'] = seasoning
        reply += checkIsReady()
        return alexa.create_response(message=reply)
    else:
        reply = "I could not find it, if you want me to read menu, say 'show pizza toppings'"
        return alexa.create_response(message=reply)        
        
''' Choosing '''


# check the order and reply to user
def checkIsReady():
    isReady, key = hasEnoughInfo()
    if isReady:
        placeOrder()
        initialzeOrder()
        return 'Order is ready, Thank you! '
    else:
        if key is 'name':
            return 'Please tell me your name. '
        if key is 'no_of_pizza':
            return 'How many pizza do you want? '
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
            return 'Please choose the seasoning for the pizza. '
        elif key is 'toppings':
            return 'Do you want any topping? '


# check the information we want before writting to sheet
def hasEnoughInfo():
    global ORDER
    for key in ORDER.keys():
        if ORDER[key] is None:
            return False, key
    return True, None


# after we get all the information, write order to the sheet
def placeOrder():
    orderHandler = OrderHandler()
    global ORDER
    orderHandler.placeOrder(ORDER)


# after ordering
def initialzeOrder():
    ORDER = OrderedDict()
    ORDER['name'] = None
    ORDER['type'] = None
    ORDER['size'] = None
    ORDER['crust'] = 'handmade'
    ORDER['sauce'] = 'barbeque'
    ORDER['bake'] = 'well done'
    ORDER['cut'] = 'pie'
    ORDER['seasoning'] = 'garlic seasoned crust'
    ORDER['toppings'] = ['bacon', 'pineapple', 'none', 'none', 'none']
    ORDER['no_of_pizza'] = None

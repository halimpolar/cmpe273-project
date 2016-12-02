from ask import alexa
from MenuHandler import MenuHandler


PIZZAS = []
SIZES = []
CRUSTS = []

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
    menuHandler = MenuHandler()
    # pizza types
    global PIZZAS
    for pizza in menuHandler.getPizzaType():
        PIZZAS.append(pizza[0])
    # pizza sizes
    global SIZES
    for size in menuHandler.getPizzaSize():
        SIZES.append(size[0])

    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Hello Welcome to the Pizza Ordering System")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")

@alexa.intent_handler("AskName")
def launch_AskName_handler(request):
    import logging
    logging.error("Im here")
    name = request.slots["name"]
	
    reply = "ordering pizza with name {}".format(name)						 
    return alexa.create_response(message=reply)

@alexa.intent_handler("ShowPizzaTypes")
def launch_ShowPizzaTypes_handler(request):
    global PIZZAS
    return alexa.create_response(message="pizza types: {}, {}".format(PIZZAS[0], PIZZAS[1]))

@alexa.intent_handler('ChoosePizzaTypes')
def get_pizza_type_handler(request):
    reply=""
    
    pizza_type = request.slots["pizza"]

    if pizza_type == None:
        reply = reply + "I could not find it, if you want me to read menu, say show pizza menu"

    global PIZZAS
    if pizza_type in PIZZAS:
        reply = reply +"What size do you want? Say show pizza size for the sizing options"

    return alexa.create_response(reply,end_session=False)

@alexa.intent_handler("ShowPizzaSizes")
def launch_ShowPizzaSizes_handler(request):
    global SIZES
    return alexa.create_response(message="pizza sizes: {}, {}".format(SIZES[0], SIZES[1]))

@alexa.intent_handler('ChoosePizzaSizes')
def get_pizza_size_handler(request):
    reply=""
    
    size_type = request.slots["size"]

    if size_type == None:
        reply = reply + "I could not find it, if you want me to read the pizza size, say show pizza size"

    global SIZES
    if size_type in SIZES:
        reply = reply +"What crust do you want? Say show pizza crust for the crust options"

    return alexa.create_response(reply,end_session=False, card_obj=card)

@alexa.intent_handler('ChoosePizzaCrusts')
def get_pizza_crust_handler(request):
    reply=""
    
    crust_type = request.slots["crust"]

    if crust_type == None:
        reply = reply + "I could not find it, if you want me to read the crust choices, say show crust options

    global CRUSTS
    if crust_type in CRUSTS:
        reply = reply +"Do you want to add any toppings?"

    return alexa.create_response(reply,end_session=False, card_obj=card)


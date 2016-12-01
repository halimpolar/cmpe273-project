from ask import alexa
from MenuHandler import MenuHandler


PIZZAS = []
SIZES = []
CRUSTS = []
'''
PIZZAS = ['extravaganzza']
SIZES = ['small', 'medium', 'large', 'extra large']
CRUSTS = ['handtossed', 'handmadepan', 'crunchythincrust','brooklynstyle','glutenfree']
'''


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


@alexa.intent_handler("ShowPizzaTypes")
def launch_ShowPizzaTypes_handler(request):
    global PIZZAS
    return alexa.create_response(message="pizza types: {}, {}".format(PIZZAS[0], PIZZAS[1]))


@alexa.intent_handler("ShowPizzaSizes")
def launch_ShowPizzaSizes_handler(request):
    global SIZES
    return alexa.create_response(message="pizza sizes: {}, {}".format(SIZES[0], SIZES[1]))


@alexa.intent_handler('pizzaorder')
def get_takeone_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    reply =""
    # Get variables like userId, slots, intent name etc from the 'Request' object
    pizza_type = request.slots["pizza"]
    size = request.slots["size"]
    menu = request.slots["menu"]
    customize = request.slots["customize"]
    crust = request.slots["crust"]

    card = alexa.create_card(title="pizza order activated", subtitle=None,
                             content="asked alexa to order pizza")

    if menu == "menu":
        reply = reply +"you can order: {0}".format(pizzas)

    if pizza_type == None and size == None and menu == None and customize == None and crust == None:
        reply = reply + "I could not find it, if you want me to read menu, say  provide menu"

    if pizza_type in pizzas:
        if size == None and crust == None:
            reply = reply +"Do you want to customize? say yes customize or say don't customize"
        else:
            reply = reply + "ordering pizza {0}".format(pizza_type)

    if customize!= None:
        if customize == "yes":
            reply = reply + "what crust do you want?Say hand tossed crust or handmade pan crust or crunchy thin crust or brooklyn stye crust or gluten free crust"
        else:
            reply = reply +" with hand tossed crust and size large"


    if size != None:
        if size in sizes:
            reply = reply +" with size for your order {0}".format(size)
        else:
            reply = reply + "But i didnt get your size, please say size small, medium, large or extra large"

    if crust != None:
        if crust in crusts:
            reply = reply+"crust is {0}".format(crust)

        else:
            reply =reply +"balh blah blah"

    return alexa.create_response(reply,end_session=False, card_obj=card)

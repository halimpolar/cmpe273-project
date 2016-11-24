from ask import alexa

def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {'user_name' : 'SomeUserName'} # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}
    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
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
    
    card = alexa.create_card(title="pizza order activated", subtitle=None,
                             content="asked alexa to order pizza")
    
    if menu == "menu":
        reply = reply +"you can order: {0}".format("EXTRAVAGANZZA")
    
    if pizza_type == None:
        reply = reply + "I could not find it, if you want me to read menu, say  provide menu"
    
    if pizza_type== "extravaganzza":
        if size == None:
            reply = reply +"which size?"
        else:
            reply = reply + "ordering pizza extravaganzza with"
    
    if size =="small" or size =="medium" or size=="large" or size =="extra large":
        reply = reply +"size for your order {0}".format(size)
       
    return alexa.create_response(reply,
                                 end_session=False, card_obj=card)

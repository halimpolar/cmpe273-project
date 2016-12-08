# Pizza Ordering System with Amazon Echo

This project serves the goal of SJSU CMPE-273 class in developing A Pizza Ordering System by using Amazon Echo Device. This project is a group project collaborated by four students.

<b>System Requirement</b>
- AWS Lambda
- Integration with Google Sheet API 
- SDK to call the Amazon Echo services and AWS component
- Amazon Echo Device
- Python 2.7

<b>What does the application do?</b>
- Order pizzas via Amazon Echo
- Users can customize the pizza according to the preference
- Ability to check the status of the pizza once it is placed
- Membership and "pizza award" system
- Order multiple pizza with the same customization in one interaction
- Save the history of the previous order 
- Cancel unfinished or wrong order
- Provide a card for order clarification

<b>Integration with Google API</b>
- Follow the instructions from Google for obtaining the API key
- Download the key you obtaining from Google
- Put the key into folder and name it with the name: 'Alexa_Pizza.json'

<b>How to test it?</b>
- Setup the Amazon Lambda environment
- Upload 'Pizza_Lambda.zip' to Lambda
- Verify the schema and utterances are configured properly following alexa_schema and output
- Load the customized slots accordingly
- Wrap the lambda function and hook the Amazon Echo Device
- Use https://docs.google.com/spreadsheets/d/1rJ6-8LPsQJFXMeQVC-RfruSuF5IQO57Oujvl2FHjgR8/ for layout of different sheets or set up your own google sheet.  
- Setup the Amazon Echo Device and you can start interacting with it
- Follow the Interaction.txt to provide the right utterance  


  * Custom Slots:  (you can add more in name type, but if you add more in any other slots, need to change ActualMenu sheet as well  
    * Type ----- Values  	
    * crust_type ----- Hand Tossed | Handmade | Crunchy Thin Crust | Gluten Free  
    * name_type ----- Polar | Vimmi | Quang | Harry    
    * pizza_type ----- Extravaganzza | Meatzza | Philly Cheese Steak | Pacific Veggie | Honolulu Hawaiian | Deluxe | Cali Chicken Bacon Ranch | Buffalo Chicken | Ultimate Pepperoni | Memphis Barbecue Chicken | Wisconsin Six Challenge | Spinach and Feta   
    * size_type ----- Small | Medium | Large | Extra Large  
    * bake_type ----- Well Done | Normal  
    * sauce_type ----- Robust Inspired Tomato | Hearty Marinara | Barbecue | Garlic Parmesan White | Alfredo   
    * cut_type ----- Pie | Square | Uncut  
    * topping_type ----- Pepperoni | Sliced Italian Sausage | Philly Steak | Bacon | Premium Chicken | Italian Sausage | Beef | Ham | Salami | Cheddar Cheese | Shredded Parmesan Asiago | Banana Peppers | Garlic | Pineapple | Roasted Red Peppers | Tomatoes | Hot Sauce | Feta Cheese | Shredded Provolone Cheese | Black Olives | Green Peppers | Mushrooms | Onions | Spinach | Diced Tomatoes   

<b>Contributing Members: </b>
- Polar Halim
- Quang Pham
- Vimmi Swami
- Yu-Chen Ku

<b>Team Flash<b>  
San Jose State University - Fall 2016

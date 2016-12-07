# Pizza Ordering System with Amazon Echo

This project serves the goal of SJSU CMPE-273 class in developing A Pizza Ordering System by using Amazon Echo Device. This project a group project collaborated by four students.

<b>System Requirement</b>
- AWS Lambda
- Integration with Google Sheet API 
- SDK to call the Amazon Echo services and AWS component
- Amazon Echo Device
- Python 2.7

<b>What does it application do?</b>
- Order pizzas via Amazon Echo
- Users can customize the pizza according to the preference
- Ability to check the status of the pizza once it is placed
- Membership and "pizza award" system
- Order multiple pizza with the same customization in one interaction
- Save the history of the previous order 
- Cancel unfinished or wrong order
- Provide a card for order clarification

<b>How to test it?</b>
- Setup the Amazon Lambda environment
- Upload 'Pizza_Lambda.zip' to Lambda
- Verify the schema and utterances are configured properly following alexa_schema and output
- Load the customized slots accordingly:

  * Custom Slots:  
    * Type ----- Values  	
    * crust_type ----- Hand Tossed | Handmade | Crunchy Thin Crust | Brooklyn Style | Gluten Free  
    * name_type ----- name  
    * pizza_type ----- Extravaganzza | Meatzza | Philly Cheese Steak | Pacific Veggie | Honolulu Hawaiian | Deluxe | Cali Chicken Bacon Ranch | Buffalo Chicken | Ultimate Pepperoni | Memphis BBQ Chicken | Wisconsin Six Challenge | Spinach and Feta   
    * size_type ----- Small | Medium | Large | Extra Large  
    * bake_type ----- Well Done | Normal  
    * sauce_type ----- Robust Inspired Tomato | Hearty Marinara | Barbeque | Garlic Parmesan White | Alfredo   
    * cut_type ----- Pie | Square | Uncut  
    * topping_type ----- Pepperoni | Sliced Italian Sausage | Philly Steak | Bacon | Premium Chicken | Italian Sausage | Beef | Ham | Salami | Cheddar Cheese | Shredded Parmesan Asiago | Banana Peppers | Garlic | Jalapeno Peppers | Pineapple | Roasted Red Peppers | Tomatoes | Hot Sauce | Feta Cheese | Shredded Provolone Cheese | Black Olives | Green Peppers | Mushrooms | Onions | Spinach | Diced Tomatoes   

<b>Contributing Members: </b>
- Polar Halim
- Quang Pham
- Vimmi Swami
- Yu-Chen Ku


San Jose State University - Fall 2016

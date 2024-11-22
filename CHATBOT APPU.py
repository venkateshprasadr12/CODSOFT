import random
from datetime import datetime

def simple_chatbot():
    print("Hello! I'm a simple chatbot. What's your name?")
    user_name = input("You: ")
    user_preferences = {}
    
    print(f"Chatbot: Nice to meet you, {user_name}! How can I help you today?")
    
    while True:
        user_input = input("You: ").lower()
        
        # Predefined responses based on user input
        if "hello" in user_input or "hi" in user_input:
            print(f"Chatbot: Hi there, {user_name}! How can I assist you?")
        elif "how are you" in user_input:
            print("Chatbot: I'm just a computer program, but thanks for asking! How are you?")
        elif "what is your name" in user_input:
            print("Chatbot: I'm a simple chatbot created to help you.")
        elif "help" in user_input:
            print("Chatbot: Sure! What do you need help with?")
        elif "bye" in user_input or "exit" in user_input:
            print("Chatbot: Goodbye! Have a great day!")
            break
        elif "weather" in user_input:
            print("Chatbot: I'm not sure about the weather, but you can check a weather website.")
        elif "time" in user_input:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"Chatbot: The current time is {current_time}.")
        elif "favorite" in user_input:
            if "color" in user_input:
                color = input("Chatbot: What's your favorite color? ")
                user_preferences['color'] = color
                print(f"Chatbot: Nice! I will remember that your favorite color is {color}.")
            elif "food" in user_input:
                food = input("Chatbot: What's your favorite food? ")
                user_preferences['food'] = food
                print(f"Chatbot: Great! I will remember that your favorite food is {food}.")
            else:
                print("Chatbot: I can remember your favorite color or food. Which one would you like to share?")
        elif "tell me a joke" in user_input:
            jokes = [
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call fake spaghetti? An impasta!"
            ]
            print(f"Chatbot: {random.choice(jokes)}")
        elif "sad" in user_input or "bad" in user_input:
            print("Chatbot: I'm sorry to hear that. If you want to talk about it, I'm here to listen.")
        elif "happy" in user_input or "good" in user_input:
            print("Chatbot: That's great to hear! What made you feel that way?")
        elif "fun fact" in user_input:
            facts = [
                "Did you know honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible!",
                "Bananas are berries, but strawberries aren't!",
                "Octopuses have three hearts!"
            ]
            print(f"Chatbot: {random.choice(facts)}")
        elif "feedback" in user_input:
            feedback = input("Chatbot: I appreciate your feedback! What do you think about my responses? ")
            print(f"Chatbot: Thank you for your feedback: '{feedback}'. I'll try to improve!")
        else:
            print("Chatbot: I'm sorry, I didn't understand that. Can you please rephrase?")

# Run the chatbot
simple_chatbot()
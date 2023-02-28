import telebot

bot = telebot.TeleBot('6127656044:AAEX2I3jBS7b3XkdyGHWSXoC92SEgedYQ20')

# Define the state of the conversation for each user
user_state = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to MathBot! I can perform basic math operations. To use me, simply send me a message with the math operation you want to perform (e.g. 'add', 'subtract', 'multiply', or 'divide').")

@bot.message_handler(func=lambda message: message.text.lower() in ['add', 'subtract', 'multiply', 'divide'])
def start_math_operation(message):
    # Save the user's selected math operation and update their state to the next step
    user_state[message.chat.id] = {'operation': message.text.lower(), 'step': 1}
    bot.reply_to(message, f"Sure, what is the first operand?")

@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id]['step'] == 1)
def get_first_operand(message):
    # Save the user's first operand and update their state to the next step
    user_state[message.chat.id]['first_operand'] = message.text
    user_state[message.chat.id]['step'] = 2
    bot.reply_to(message, f"Great, what is the second operand?")

@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id]['step'] == 2)
def calculate_result(message):
    # Calculate the result based on the user's selected operation and operands
    operation = user_state[message.chat.id]['operation']
    first_operand = user_state[message.chat.id]['first_operand']
    second_operand = message.text
    try:
        if operation == 'add':
            result = float(first_operand) + float(second_operand)
            bot.reply_to(message, f"The sum of {first_operand} and {second_operand} is {result}. Type 'start another operation' to begin another operation.")
        elif operation == 'subtract':
            result = float(first_operand) - float(second_operand)
            bot.reply_to(message, f"The difference between {first_operand} and {second_operand} is {result}. Type 'start another operation' to begin another operation.")
        elif operation == 'multiply':
            result = float(first_operand) * float(second_operand)
            bot.reply_to(message, f"The product of {first_operand} and {second_operand} is {result}. Type 'start another operation' to begin another operation.")
        elif operation == 'divide':
            result = float(first_operand) / float(second_operand)
            bot.reply_to(message, f"The quotient of {first_operand} and {second_operand} is {result}. Type 'start another operation' to begin another operation.")
        # Reset the user's state to start a new conversation
        user_state[message.chat.id]['step'] = 0
    except:
        bot.reply_to(message, "can't be 0, enter a valid operand!")
        # Reset the user's state to start a new conversation

@bot.message_handler(func=lambda message: message.text.lower() == 'start another operation')
def start_new_operation(message):
    # Clear the user's state to start a new conversation
    user_state[message.chat.id] = {'step': 0}
    bot.reply_to(message, "Sure, what mathematical operation do you want to perform?")
    
bot.polling()

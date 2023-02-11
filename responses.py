import random

def handle_response(message) ->str:
    message = message.lower()

    if message.startswith("roll"):
        number = int(message.split()[-1])
        return random.randint(0, number)
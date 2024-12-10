import random
import string

class Service():
    
    def generate_random_alphanumeric(self):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(5))
        return random_string
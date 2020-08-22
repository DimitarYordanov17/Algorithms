# Diffie-Hellman key exchange Python implementation. @DimitarYordanov
import math
import time
import random

class Person:
    g = 0
    n = 0
    
    def __init__(self, max_private_number):
        self.private_key = random.choice([i for i in range(2, max_private_number + 1) if is_prime(i)])
        self.public_key = 0
        self.other_info = []
        self.final_key = 0
        
    def generate_public_key(self):
        self.public_key = (Person.g ** self.private_key) % Person.n
            
    def generate_final_key(self):
        self.final_key = (self.other_info[0] ** self.private_key) % Person.n
    
    def __repr__(self):
        return f"""
            private key: {self.private_key}
            public key: {self.public_key}
            other info: {self.other_info}
            final key: {self.final_key}"""
    
def is_prime(n):
    # Copied from stack overflow
    if n < 2: 
         return False;
    if n % 2 == 0:             
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

def get_starting_parameters(max_g, min_n, max_n):
    g = random.choice([i for i in range(2, max_g + 1) if is_prime(i)])
    n = random.choice([i for i in range(min_n, max_n + 1) if is_prime(i)])
    
    return g, n

def attacker_brute_force(user, final_key):
    start_time = time.time()
    
    for power in range(1, Person.n):
        if (user.public_key ** power) % Person.n == final_key:
            print(f"It took {time.time() - start_time} seconds for the attacker to bruteforce the key, key is {final_key}")
            return

# Driver code:
        
# Step 1. Generate random g and n
parameters = get_starting_parameters(10, 100000, 1000000)

Person.g = parameters[0]
Person.n = parameters[1]

# Step 2. Everybody gets a random private number (In real situation the attack wouldn't get a random number)
Allice = Person(1000)
Bob = Person(1000)
Darth = Person(1000) # Attacker

# Step 3. Allice and Bob generate their public keys

Allice.generate_public_key()
Bob.generate_public_key()

# Step 4. Allice and Bob exchange public keys, eventually Darth gets them too
Allice.other_info.append(Bob.public_key)
Bob.other_info.append(Allice.public_key)

# Darth gets both
Darth.other_info.append(Allice.public_key)
Darth.other_info.append(Bob.public_key)

# Step 5: Everybody generates their final key

Allice.generate_final_key()
Bob.generate_final_key()
Darth.generate_final_key()

# Step 6: Allice and Bob end up with the same keys, while Darth does not

print("G is", Person.g)
print("N is", Person.n)

print("Allice", Allice)
print("Bob", Bob)
print("Darth", Darth)

# Test how hard it is to bruteforce the final_key
attacker_brute_force(Bob, Allice.final_key)
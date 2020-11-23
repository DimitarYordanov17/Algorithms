# MD5 Python Implementation. @DimitarYordanov17
import numpy
import math
import random

class MD5:
    """
    A class that implements the functionality of the MD5 algorithm
    """
    
    buffers = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
    
    constants = [[0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee],
                 [0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501],
                 [0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be],
                 [0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821],
                 [0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa],
                 [0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8],
                 [0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed],
                 [0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a],
                 [0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c],
                 [0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70],
                 [0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05],
                 [0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665],
                 [0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039],
                 [0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1],
                 [0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1],
                 [0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]]
    
    rounds_shift = [[7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22],
                    [5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20],
                    [4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23],
                    [6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]]
    
    def prepare_input(input_text):
        """
        Represent the input text as 512 bit blocks
        """
        
        starting_bits = "".join([numpy.binary_repr(ord(char), width=8) for char in input_text])
        bits_needed = (448 + (512 * (len(starting_bits) // 448))) - len(starting_bits)
        
        if len(starting_bits) == 0: # Empty input text
            bits_needed = 960
        
        extended_form = starting_bits
        
        extended_form += ("1" if bits_needed > 0 else "")
        extended_form += ("0" * (bits_needed - 1) if bits_needed > 1 else "")
        extended_form += numpy.binary_repr(len(starting_bits), width=64)
        
        blocks = [extended_form[i:i+512] for i in range(0, len(extended_form), 512)]
        
        return blocks

    def process_buffer(buffers, function, word, round_count, operation_count):
        """
        Returns the modified buffer after the applyment of operations
        """
        
        return buffers[1] + MD5.left_rotate(buffers[0] + function(buffers[1], buffers[2], buffers[3]) + MD5.constants[operation_count][round_count] ^ int(word, 2), MD5.rounds_shift[round_count][operation_count])
        
    def process_block(block, buffers):
        """
        Returns the modified buffers after 4x16 rounds
        """
        
        A = buffers[0]
        B = buffers[1]
        C = buffers[2]
        D = buffers[3]
        
        words = [block[i:i+32] for i in range(0, len(block), 32)]
        
        functions = [MD5.f, MD5.g, MD5.h, MD5.i]

        for round_count in range(4):
            for operation_count in range(16):
                function = functions[round_count]

                
                A, B, C, D = D, MD5.process_buffer([A, B, C, D], function, words[operation_count], round_count, operation_count), B, C
        
        A = (buffers[0] + A)  % (2 ** 32)
        B = (buffers[1] + B)  % (2 ** 32)
        C = (buffers[2] + C)  % (2 ** 32)
        D = (buffers[3] + D)  % (2 ** 32)

        return [A, B, C, D]
    
    def hash(message):
        """
        Returns the hash of a message (buffers are stabilized so the resulting hash is 32 hex symbols)
        """
        
        blocks = MD5.prepare_input(message)
        
        buffers = MD5.buffers

        for block in blocks:
            buffers = MD5.process_block(block, buffers)
        
        buffers = [buffer for buffer in buffers]
        
        stabilized_buffers = MD5.stabilize_buffers(buffers)
        
        resulting_hash = "".join(stabilized_buffers)
        
        return resulting_hash
    
    def stabilize_buffers(buffers):
        """
        Appends a hex char, dependent on the buffer, if needed (hex_length != 8)
        """
        
        stabilized_buffers = []
        
        for buffer in buffers:
            hex_buffer = hex(buffer)[2:]
            hex_length = len(hex_buffer)
            
            if hex_length != 8:
                hex_buffer += hex(buffer % 15)[2:]
            
            stabilized_buffers.append(hex_buffer)
            
        return stabilized_buffers
        
    # \/ Bitwise operations functions \/
    
    def f(x, y, z):
        return (x & y) | ((~x) & z)
    
    def g(x, y, z):
        return (x & z) | (y & (~z))
    
    def h(x, y, z):
        return x ^ y ^ z
    
    def i(x, y, z):
        return y ^ (x | (~z))
    
    def left_rotate(value, s):
        return (value << s) | (value >> (32 - s))
    
# Driver code:

# Long text example
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
text_hash = MD5.hash(text)
print(text_hash)

text1 = "Hello, I implemented this algorithm on 11/23/2020 for several hours and I am happy about it"
text2 = "Hello, I implemented this algorithm on 11/23/2020 for several hours and I am happy about it."

text1_hash = MD5.hash(text1)
text2_hash = MD5.hash(text2)

# Here you can see that just a dot in the input changes the whole hash
print("~~~~~~~~~~~~~~~~~~~~~~~~")
print(text1_hash)
print(text2_hash)

# Run-length Compression (Encoding) Python implementation. @DimitarYordanov17
import re

def compress(text):
    """
    Returns the run-length encoded version of the text
    (numbers after symbols, length = 1 is skipped)
    """
    result = ""
    
    current_letter_details = [text[0], 0] # Current letter and it's count till now
    
    for letter in text:
        if letter == current_letter_details[0]: # Same letter
            current_letter_details[1] += 1
        else: # Different letter
            # Add the previous letter details to the result string
            if current_letter_details[1] == 1:
                current_letter_details[1] = ""
            result += current_letter_details[0] + str(current_letter_details[1])
            
            # Reset and start again
            current_letter_details = [letter, 1]
    
    if current_letter_details[1] == 1:
        current_letter_details[1] = ""
    result += current_letter_details[0] + str(current_letter_details[1])
    
    return result

def decompress(text):
    """
    Decodes the text using run-length encoding
    """
    result = ""
    
    combinations = re.findall(r'[A-Z][0-9]*', text)
    
    for combination in combinations:
        letter = combination[0]
        try:
            number = int(combination[1:])
        except:
            number = 1
        result += letter * number
        
    return result

# Driver code:

compressed_text = compress("ATTCCGGGG")
print(compressed_text)
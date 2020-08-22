# HuffmanCompression (Coding) Python implementation. @DimitarYordanov17
class Node:
    """
    Node with 2 branches
    """
    def __init__(self, left, value, right):
        self.left = left
        self.value = value
        self.right = right
    
class Leaf:
    """
    Char connected to a branch
    """
    def __init__(self, char):
        self.char = char
    
class Huffman:
    """
    Main operations class
    """
    def __init__(self, text):
        """
        Initialize the frequency_table -> tree -> code_table
        """
        self.text = text
        self.frequency_table = self.get_frequency_table()
        self.tree = self.create_huffman_tree()
        self.code_table = self.get_code_table()

    def compress(self):
        """
        Return compressed text (substituted with the code table)
        """
        compressed_text = ""
        
        for char in self.text:
            compressed_text += self.code_table[char]
        
        return compressed_text
    
    def get_frequency_table(self):
        """
        Return the char: occurrences dictionary table
        """
        table = dict()
        unique_text = set(self.text)
        
        for current_char in unique_text:
            occurrences = self.text.count(current_char)
            table[current_char] = occurrences
            
        return table
    
    def get_code_table(self):
        """
        Return code table via the find_leaf function
        """
        table = {c: self.find_leaf(c) for c in self.text}
        return table
    
    def create_huffman_tree(self):
        """
        Initialize the huffman tree (List with nodes, containing nodes, containing nodes and so on)
        """
        tree = self.frequency_table.items()
        
        while len(tree) != 1: # a.k.a while there is only one node in the list and all others are nested
            tree = sorted(tree, key=lambda x: x.value if x.__class__.__name__ == "Node" else x[1], reverse=True)
            left_part = tree[-1] # Get the smallest node/(char/occurences) pair
            right_part = tree[-2]
            
            # Check if a Node object or a char/occurrences pair and initialize a new node object, from the left and right ones
            
            if left_part.__class__.__name__ == 'tuple' and right_part.__class__.__name__ == 'tuple': # Char/occurrences
                value = left_part[1] + right_part[1]
                new_node = Node(Leaf(left_part[0]), value, Leaf(right_part[0]))
            elif  left_part.__class__.__name__ == 'tuple' or right_part.__class__.__name__ == 'tuple': # Char/occurence and Node
                tuple_part = "left" if left_part.__class__.__name__ == 'tuple' else "right"
                
                new_node_value = 0
                
                if tuple_part == "left":
                    node_value = right_part.value
                    part_value = left_part[1]
                    new_node = Node(Leaf(left_part[0]), node_value + part_value, right_part)
                else:
                    node_value = left_part.value
                    part_value = right_part[1]
                    new_node = Node(left_part, node_value + part_value, Leaf(right_part[0]))
                    
            else: # Two nodes
                new_node_value = left_part.value + right_part.value
                new_node = Node(left_part, new_node_value, right_part)
            
            tree.pop() # Remove the elements used to create the new node 
            tree.pop()
            
            # Add the new node to the tree
            tree.append(new_node)    
        
        return tree
    
    def find_leaf(self, char):
        """
        Return the code of a char (level traversal, then a traceback)
        """
        trace_back_nodes = [["empty_node"]]
        last_row_nodes = [self.tree[0]] # a.k.a starting nodes
        result = ""
        
        found = False
        starting = True
        
        # 1: Find leaf
        while not found:
            # Every new iteration, init a new current nodes list(row nodes)
            # Every next block should have len(last_block (only nodes)) * 2 elements 
            current_nodes = []
            
            for element in last_row_nodes:
                if element.__class__.__name__ == "Node":
                    current_nodes.append(element.left)
                    current_nodes.append(element.right)
            
            found_index = 0
            for i in current_nodes:
                if i.__class__.__name__ == "Leaf":
                    if i.char == char:
                        found = True
                        break
                found_index += 1
            
            # Make a row representation
        
            if found:
                traceback_list = ["empty_node" if i.__class__.__name__ == "Node" else ("char" if i.char == char else "leaf") for i in current_nodes]
                trace_back_nodes.append(traceback_list)
                break
                        
            last_row_nodes = current_nodes
            trace_back_nodes.append(["empty_node" if i.__class__.__name__ == "Node" else ("char" if i.char == char else "leaf") for i in current_nodes])
                
            
        # 2: Traceback
        
        trace_back_nodes.reverse()
        char_index = trace_back_nodes[0].index("char")
        
        row_index = 0
        for current_row in trace_back_nodes[:-1]:
            # Take care of the turn
            current_turn = char_index % 2
            result += str(current_turn)
            
            # 1: Divide current_row into sublists_to_be_made sublists
            sublists_to_be_made = 0
            if row_index != len(trace_back_nodes) - 1:
                sublists_to_be_made = len([i for i in trace_back_nodes[row_index + 1] if i == "empty_node"])
            
            sublists = []
            for i in range(0, sublists_to_be_made * 2, 2):
                if i != len(current_row):
                    current_sublist = [current_row[i], current_row[i + 1]]
                    sublists.append(current_sublist)
            
            # -------------------------------------------------------------
            # 2: Find new index and mutate the next row
            new_char_list = [1 if "char" in i else 0 for i in sublists]
            char_index = new_char_list.index(1) if (1 in new_char_list) else 0
            
            index_counter = 0
            seen_nodes = 0
            if row_index != len(trace_back_nodes) - 1:
                for i in trace_back_nodes[row_index + 1]:
                    if i == "empty_node":
                        seen_nodes += 1
                    
                    if seen_nodes == char_index + 1:
                        break
                        
                    index_counter += 1
                        
            char_index = index_counter
            
            if row_index != len(trace_back_nodes) - 1:
                trace_back_nodes[row_index + 1][char_index] = "char"
            
            row_index += 1

        # 3: Return result
        return result
            
# Driver code:

text = "It took me roughly 5 minutes to understand the algorithm and a lot more to implement it, I learned much about trees as data structures during the implementation"

huffman_text = Huffman(text)

compressed_text = huffman_text.compress()

print(compressed_text)

uncompressed_memory = len(text) * 8
compressed_memory = len(compressed_text)

print(f"Bits it takes to store the normal text: {uncompressed_memory}")
print(f"Bits it takes to store the compressed text: {compressed_memory}")
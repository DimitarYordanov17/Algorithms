# AES Python implementation. @DimitarYordanov17
from copy import copy

sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

affine_transformation_matrix = [
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1]
]

mix_columns_matrix = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2 ,3],
    [3, 1, 1, 2],
]

rcon_matrix = [
    [0x01, 0x0, 0x0, 0x0],
    [0x02, 0x0, 0x0, 0x0],
    [0x04, 0x0, 0x0, 0x0],
    [0x08, 0x0, 0x0, 0x0],
    [0x10, 0x0, 0x0, 0x0],
    [0x20, 0x0, 0x0, 0x0],
    [0x40, 0x0, 0x0, 0x0],
    [0x80, 0x0, 0x0, 0x0],
    [0x1b, 0x0, 0x0, 0x0],
    [0x36, 0x0, 0x0, 0x0]
]

def message_to_matrix(message: str):
    """
    Transforms and returns the 128 bit text to 4x4 (16) elements list (matrix)
    """

    matrix = []
    for i in range(0, len(message), 4):
        matrix.append([ord(message[i]) for i in range(i, i + 4)])

    return matrix

def matrix_to_message(matrix: list):
    """
    Transforms and returns the 4x4 (16) matrix to 128 bit message
    """

    return "".join([chr(x) for y in matrix for x in y])

def encrypt(message: str, key: str):
    key_length = len(str(key))
    rounds = 10 if key_length == 16 else (12 if key_length == 24 else 14)
    
    cipher = Matrix(message, key)
    
    cipher.add_round_key(0)
    
    for i in range(1, rounds + 1):
        cipher.sub_bytes()
        cipher.shift_rows()
        
        if i != rounds:
           cipher.mix_columns()
        
        cipher.add_round_key(i)
          
    return cipher

class Matrix:
    """
    Main class to do operations on
    """

    def __init__(self, init_message: str, key: str):
        """
        Initializes an object with matrix (message), key and round key
        """
        self.matrix = message_to_matrix(init_message)
        self.key = message_to_matrix(key)
        self.round_key = message_to_matrix(key)

    def sub_bytes(self):
        """
        Substitutes elements in the object matrix with the s-box
        """
        for row, index in zip(self.matrix, range(4)):
            self.matrix[index] = [sbox[element]for element in row]

    def shift_rows(self):
        """
        Shifts the rows to the left with n - 1 (n = row number)
        """
        # [1, 2, 3, 4] -> [2, 3, 4, 1]
        self.matrix[1] = [self.matrix[1][1], self.matrix[1][2], self.matrix[1][3], self.matrix[1][0]]
        # [1, 2, 3, 4] -> [3, 4, 1, 2]
        self.matrix[2] = [self.matrix[2][2], self.matrix[2][3], self.matrix[2][0], self.matrix[2][1]]
        #[1, 2, 3, 4] -> [4, 1, 2, 3]
        self.matrix[3] = [self.matrix[3][3], self.matrix[3][0], self.matrix[3][1], self.matrix[3][2]]

    def galoisMult(self, a, b):
        p = 0
        hiBitSet = 0
        for i in range(8):
            if b & 1 == 1:
                p ^= a
            hiBitSet = a & 0x80
            a <<= 1
            if hiBitSet == 0x80:
                a ^= 0x1b
            b >>= 1
        return p % 256

    def mix_column(self, column):
        temp = copy(column)
        column[0] = self.galoisMult(temp[0],2) ^ self.galoisMult(temp[3],1) ^ \
                    self.galoisMult(temp[2],1) ^ self.galoisMult(temp[1],3)
        column[1] = self.galoisMult(temp[1],2) ^ self.galoisMult(temp[0],1) ^ \
                    self.galoisMult(temp[3],1) ^ self.galoisMult(temp[2],3)
        column[2] = self.galoisMult(temp[2],2) ^ self.galoisMult(temp[1],1) ^ \
                    self.galoisMult(temp[0],1) ^ self.galoisMult(temp[3],3)
        column[3] = self.galoisMult(temp[3],2) ^ self.galoisMult(temp[2],1) ^ \
                    self.galoisMult(temp[1],1) ^ self.galoisMult(temp[0],3)

        return column[0], column[1], column[2], column[3]

    def mix_columns(self):
        """
        Returns the columns, mixed (multiplied by the const matrix, then added to the current byte)
        /galoisMult and mix_column were copied from Stack Overflow/
        """
        column1 = self.mix_column([self.matrix[0][0], self.matrix[1][0], self.matrix[2][0], self.matrix[3][0]])
        column2 = self.mix_column([self.matrix[0][1], self.matrix[1][1], self.matrix[2][1], self.matrix[3][1]])
        column3 = self.mix_column([self.matrix[0][2], self.matrix[1][2], self.matrix[2][2], self.matrix[3][2]])
        column4 = self.mix_column([self.matrix[0][3], self.matrix[1][3], self.matrix[2][3], self.matrix[3][3]])

        self.matrix[0][0], self.matrix[1][0], self.matrix[2][0], self.matrix[3][0] = column1[0], column1[1], column1[2], column1[3]
        self.matrix[0][1], self.matrix[1][1], self.matrix[2][1], self.matrix[3][1] = column2[0], column2[1], column2[2], column2[3]
        self.matrix[0][2], self.matrix[1][2], self.matrix[2][2], self.matrix[3][2] = column3[0], column3[1], column3[2], column3[3]
        self.matrix[0][3], self.matrix[1][3], self.matrix[2][3], self.matrix[3][3] = column4[0], column4[1], column4[2], column4[3]

    def get_round_key(self, rounds: int):
        """
        Returns the current round key columns 
        """
        if rounds == 0:
            column1 = [self.key[0][0], self.key[1][0], self.key[2][0], self.key[3][0]]
            column2 = [self.key[0][1], self.key[1][1], self.key[2][1], self.key[3][1]]
            column3 = [self.key[0][2], self.key[1][2], self.key[2][2], self.key[3][2]]
            column4 = [self.key[0][3], self.key[1][3], self.key[2][3], self.key[3][3]]
            return [column1, column2, column3, column4]
        else:
            rot_word = [sbox[self.round_key[1][3]], sbox[self.round_key[2][3]], sbox[self.round_key[3][3]], sbox[self.round_key[0][3]]] # Get's the m. inverse of the last column
            rcon = rcon_matrix[rounds - 1]
            previous_column1 = self.round_key[0][0], self.round_key[1][0], self.round_key[2][0], self.round_key[3][0]

            column1 = [x ^ y ^ z for x, y, z in zip(previous_column1, rot_word, rcon)]
            column2 = [x ^ y for x, y in zip(column1, [self.round_key[0][1], self.round_key[1][1], self.round_key[2][1], self.round_key[3][1]])]
            column3 = [x ^ y for x, y in zip(column2, [self.round_key[0][2], self.round_key[1][2], self.round_key[2][2], self.round_key[3][2]])]
            column4 = [x ^ y for x, y in zip(column3, [self.round_key[0][3], self.round_key[1][3], self.round_key[2][3], self.round_key[3][3]])]

            return [column1, column2, column3, column4]

    def add_round_key(self, rounds: int):
        """
        XORs the current matrix, with the columns from get_round_key, and changes the round key
        """
        columns = self.get_round_key(rounds)

        self.matrix[0][0], self.matrix[1][0], self.matrix[2][0], self.matrix[3][0] = self.matrix[0][0] ^ columns[0][0], self.matrix[1][0] ^ columns[0][1], self.matrix[2][0] ^ columns[0][2], self.matrix[3][0] ^ columns[0][3]
        self.matrix[0][1], self.matrix[1][1], self.matrix[2][1], self.matrix[3][1] = self.matrix[0][1] ^ columns[1][0], self.matrix[1][1] ^ columns[1][1], self.matrix[2][1] ^ columns[1][2], self.matrix[3][1] ^ columns[1][3]
        self.matrix[0][2], self.matrix[1][2], self.matrix[2][2], self.matrix[3][2] = self.matrix[0][2] ^ columns[2][0], self.matrix[1][2] ^ columns[2][1], self.matrix[2][2] ^ columns[2][2], self.matrix[3][2] ^ columns[2][3]
        self.matrix[0][3], self.matrix[1][3], self.matrix[2][3], self.matrix[3][3] = self.matrix[0][3] ^ columns[3][0], self.matrix[1][3] ^ columns[3][1], self.matrix[2][3] ^ columns[3][2], self.matrix[3][3] ^ columns[3][3]

        # Change current key
        self.round_key[0][0], self.round_key[1][0], self.round_key[2][0], self.round_key[3][0] = columns[0][0], columns[0][1], columns[0][2], columns[0][3]
        self.round_key[0][1], self.round_key[1][1], self.round_key[2][1], self.round_key[3][1] = columns[1][0], columns[1][1], columns[1][2], columns[1][3]
        self.round_key[0][2], self.round_key[1][2], self.round_key[2][2], self.round_key[3][2] = columns[2][0], columns[2][1], columns[2][2], columns[2][3]
        self.round_key[0][3], self.round_key[1][3], self.round_key[2][3], self.round_key[3][3] = columns[3][0], columns[3][1], columns[3][2], columns[3][3]

    def visualise(self):
        """
        Visualises the object matrix with the hex-transformed element
        """
        print("Matrix in hex:")
        for y in self.matrix:
            for x in y:
                print(hex(x)[2:], end=" | ")
            print()

    def __str__(self):
        return matrix_to_message(self.matrix)

# Driver code:

message = "Good afternoon!!"
key = "87asd5gf6h4j3kk0"

encrypted_message = encrypt(message, key)

print(encrypted_message)
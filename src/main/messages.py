import random


def generate_message(number_columns, number_bits=4):
    """
    Description : Generates a random message (list)
    Arguments :
        - number_letters: Number of letters in the message (the size of the list)
    Returns:
        - Randomly generated message (list)
    """
    message=[]
    alphabets="AZERTYUIOPQSDFGHJKLMWXCVBN1234567890"

    # Deducing the number of letters to generate by dividing by the number of bits
    number_letters = number_columns // number_bits

    # Randomly choising letters or numbers in the list
    for i in range (0, number_letters):
        ind=random.randint(0, 35)
        message.append(alphabets[ind])
    
    return message


def message_to_ternary(message, number_bits=4):
    """
    Description : Returns the message coded in ternary
    Arguments :
        - message: Message to code (list)
        - number_bits: Number of bits to code each letter
                        & by default it is equal to 4
    Returns:
        - Ternary message (list)
    """
    ternary_message=[]

    for i in message:
        ascii_value = ord(i)

        if ascii_value==0:
            ternary_char = [0]
        else:
            ternary_char = []
            # Saving the remainder of the division by 3 to deduce the ternary code
            while ascii_value != 0:
                remainder_division = ascii_value % 3
                ascii_value = ascii_value // 3
                if remainder_division == 2:
                    remainder_division = -1
                    ascii_value += 1
                ternary_char.append(remainder_division)
        
        while len(ternary_char) < number_bits:
            ternary_char.append(0)
        
        # To invert the ternary code and to have exactly the number of bits wanted
        ternary_message += ternary_char[::-1][:number_bits]

    return ternary_message


def encode_message(ternary_message, public_key):
    """
    Description : Encodes a ternary message with the given public key
    Arguments :
        - ternary_message: Message in ternary we want to encode with the key (list)
        - public_key: Key used to encode the message
    Returns:
        - Encoded message (list)
    """
    encoded_message = ternary_message[:]
    public_key_size = len(public_key)
    
    # Randomly choosing how many time to rotate the public key and andding to the message
    min_number_rotation = public_key_size-3
    max_number_rotation = public_key_size
    number_rotations = random.randint(min_number_rotation, max_number_rotation)

    # Choosing randomly the rotation value
    rotation_index = random.sample(range(0, public_key_size), number_rotations)

    for i in rotation_index:
        # Random rotation of the key
        rotated_key = public_key[i:] + public_key[:i]

        # Random choice to add or substract the kay to the message
        random_sign = random.choices([-1, 1], k=1)[0]

        for n in range (0, public_key_size):
            encoded_message[n] += random_sign * rotated_key[n]

    return encoded_message


def decode_message_private_key(encoded_message, private_key, number_bits=4):
    """
    Description : Decodes an encoded message using the private key
    Arguments :
        - encoded_message: The encoded message (list)
        - private_key: The private key used to decode (list)
    Returns:
        - Decoded ternary message (list)
    """
    public_key_size = len(private_key)
    decoded_message = encoded_message[:]

    abs_private_key=[]
    for m in private_key:
        abs_private_key.append(abs(m))
    max_index_key = abs_private_key.index(max(abs_private_key))

    while any(abs(value) > 1 for value in decoded_message):
        abs_message=[]
        for l in decoded_message:
            abs_message.append(abs(l))
        max_index_message = abs_message.index(max(abs_message))
        
        # Rotate the key to align the two columns
        if max_index_message < max_index_key:
            rotated_key = private_key[max_index_key - max_index_message:] + private_key[:max_index_key - max_index_message]
        elif max_index_message > max_index_key:
            rotated_key = private_key[public_key_size - (max_index_message - max_index_key):] + private_key[:public_key_size - (max_index_message - max_index_key)]
        else:
            rotated_key = private_key
        """
        if max_index_message < max_index_key:
            rotated_key = private_key[max_index_message:] + private_key[:max_index_message]
        elif max_index_message > max_index_key:
            rotated_key = private_key[max_index_message:] + private_key[:max_index_message]
        else:
            rotated_key = private_key
        """

        chosen_sign = 1
        if decoded_message[max_index_message]*private_key[max_index_key] > 0:
            chosen_sign = -1

        for n in range (0, public_key_size):
            decoded_message[n] += chosen_sign * rotated_key[n]
        
    return decoded_message
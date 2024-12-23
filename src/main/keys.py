import random


def generate_private_key(number_columns):
    """
    Description : Generates a private key
    Arguments :
        - number_columns: Number of columns in the private key
                        (should be equal to the size of the encoded message
                        & a multiple of the number of bits for one encoded letter)
    Returns:
        - Private key (list)
    """
    private_key=[]

    # Randomly assign to the private key values betweeen 1 and 2
    for i in range (0, number_columns):
        #private_key.append(random.randint(1, 2))
        private_key = random.choices([1, 2], weights=[10, 1], k=number_columns)

    # Randomly choose a column to be the highest value column
    highest_column_ind = random.randint(0, number_columns-1)
    highest_column_value = random.randint(7, 9)
    private_key[highest_column_ind] = highest_column_value

    # Randomly assign the sign (negative, zero or positive) to the values (with a certain weight)
    # But the highest column should not be multiplied by 0
    private_key_signs = random.choices([-1, 0, 1], weights=None, k=number_columns)
    private_key_signs[highest_column_ind] = random.choices([-1, 1], k=1)[0]

    for i in range (0, number_columns):
        private_key[i] = private_key[i] * private_key_signs[i]

    return private_key


def generate_public_key(private_key):
    """
    Description : Generates a public key using a private key
    Arguments :
        - private_key: Private key used to generate the public key
    Returns:
        - Public key (list)
    """
    public_key=[]
    public_key_size = len(private_key)
    
    for i in range (0, public_key_size):
        public_key.append(0)

    # Genarating the number of columns with high value (nagetive or positive)
    min_number_high_columns = public_key_size-3
    max_number_high_columns = public_key_size-2
    number_high_columns = random.randint(min_number_high_columns, max_number_high_columns)

    # Choosing randomly the columns with highest values (negatively or positively)
    high_columns_index = random.sample(range(0, public_key_size), number_high_columns)

    # Adding or substracting the private key to the public key shifting to have the highest value column in the chosen columns
    abs_private_key=[]

    for m in private_key:
        abs_private_key.append(abs(m))
    
    max_index = abs_private_key.index(max(abs_private_key))

    for k in high_columns_index:

        if k < max_index:
            shifted_private_key = private_key[k:] + private_key[:k]
        elif k > max_index:
            shifted_private_key = private_key[k-1:] + private_key[:k-1]
        else:
            shifted_private_key = private_key
        
        chosen_sign = random.choices([-1, 1], k=1)[0]

        for n in range (0, public_key_size):
            public_key[n] += chosen_sign * shifted_private_key[n]
    
    return public_key
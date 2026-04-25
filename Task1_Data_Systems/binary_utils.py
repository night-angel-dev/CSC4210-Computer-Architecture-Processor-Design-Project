"""
binary_utils.py
Main binary operations for 32-bit signed intger conversions.
Provides low-level binary manipulation functions.

"""



def twos_complement(binary_str):
    """
    Converts a binary to its negative version using twos complement logic
    
    @param binary_str - binary being converted to negative version
    @return - negative version of positive binary
    """
    
    # Step one invert all bits
    inverted_bits = []
    
    for bit in binary_str:
        
        if bit == '0':
            inverted_bits.append('1')
        else:
            inverted_bits.append('0')
            
    inverted = ''.join(inverted_bits)
    
    # # debug check
    # print(f"After inversion: {inverted}")
    
    
    # Step 2: Add 1 32 bits long
    one_in_binary = '00000000000000000000000000000001'
    
    twos_comp = binary_addition(inverted, one_in_binary)
    
    return twos_comp


def binary_addition(binary_str1, binary_str2):
    """
    Add two binary strings using bit by bit addition with carry.

    @param binary_str1 - First binary string
    @param binary_str2 - Second binary string
    @return - Sum as binary string

    """
    # first we need to make sure both strings are the same length
    max_len = max( len( binary_str1 ), len( binary_str2 ) )
    binary1 = binary_str1.zfill(max_len)
    binary2 = binary_str2.zfill(max_len)
    
    
    # Start from rlight most to lesftmost
    result = []
    carry = 0
    
    
    # Loop from last to first index
    for i in range(max_len - 1, -1, -1):
        
        # gets bits of position i
        bit1 = int(binary1[i])
        bit2 = int(binary2[i])
        
        # Calculatute sum 
        total = bit1 + bit2 + carry
        
        # Determine result bit and new carry
        result_bit = total % 2
        carry = total // 2
        
        # Insert at the begining
        result.insert(0, str(result_bit))
    
    
    # Catching problem if there is a final carry
    if carry:
        result.insert(0, str(carry))
        
    result_str = ''.join(result)
        
    # Mask to 32 bits 
    if len(result_str) > 32:
        result_str = result_str[-32:]
    elif len(result_str) < 32:
        result_str = result_str.zfill(32)
        
    # # debug check
    # print(f"Result {result_str} ")
    
    
    return result_str


def binary_to_hexadecimal(value, prefix = "0x"):
    """
    This method converts a binary value to a hexadecimal value by 
    splitting from left to right the binary bits into groups of four and give those
    groups a distinct hexadecimal values

    @param value - binary value being converted to hexadecimal value
    @param prefix - hexadecimal prefix (defualt "0x")
    @return - the hexadecimal value 
    """
    # Make a map to compare to 
    binary_to_hex_map = {
        "0000" : "0", "0001" : "1", "0010" : "2", "0011": "3",
        "0100" : "4", "0101" : "5", "0110" : "6", "0111" : "7",
        "1000" : "8", "1001" : "9", "1010" : "A", "1011" : "B",
        "1100" : "C", "1101" : "D", "1110" : "E", "1111" : "F"   
    }
    
    hex_digits = []
    
    
    # Retrieve 4 bit groups and identify and append correct hex value to hex digits
    for i in range(0, 32, 4):
        chunk = value[i : i + 4]
        hex_digit = binary_to_hex_map[chunk]
        hex_digits.append(hex_digit)
        
        
    # Join to string
    hex_str = ''.join(hex_digits)
    
    return f"{prefix}{hex_str}"


def binary_to_decimal(value):
    """
    Converts a 32 bit binary value to decimal value

    @param value - Binary value being converted to decimal
    @return - Binary's decimal value
    """
    # value should be a string so we can iterate through it and find the decimal value
    decimal_value = 0
    isNegative = False
    
    # check if negative
    if value[0] == '1':
        isNegative = True
        
    # if binary is negative, applying tow complements should make it positive
    if isNegative:
        value = twos_complement(value)
        
    decimal_value = 0
    
    # should go from right to left
    for i in range(len(value) - 1, -1, -1 ):
        
        if value[i] == '1':
            
            power = 31 - i
            decimal_value += 2 ** power
            
    if isNegative:
        decimal_value = -1 * decimal_value        
    
    return decimal_value


def decimal_to_padded_binary(value, bit_width = 32):
    """
    Converts a decimal integer to padded binary string using two's complement if necessary.

    @param value - decimal integer value 
    @param bit_width - Number of bits default 32
    @return - padded binary string
    """
    # Handle case of 0
    if value == 0:
        return "0" * bit_width
    
    # remember if negative
    is_negative = value < 0 # True or False
    
    # Doing the division method so we need the absolutue value
    abs_value = abs(value)
    
    # Convert absolutte valeu to binary
    binary_str = decimal_to_binary(abs_value)
    
    # Pad and apply sign representation    
    return pad_and_apply_sign(binary_str, is_negative, bit_width)


def decimal_to_binary(value):
    """
    Converts a decimal integer to binary (no padding, no sign handling)
    
    @param value - non-negative integer
    @return - Binary string without leading zeros
    """
    
    if value == 0:
        return "0"
    
    binary_digits = []
    temp = value
    
    while temp > 0:
        remainder = temp % 2 # least significant bit
        binary_digits.append(str(remainder))
        temp = temp // 2 # int division by 2
        
    # We need to reverse that to get the correct order of binary
    binary_digits.reverse() # thank you python
    
    return ''.join(binary_digits)


def pad_and_apply_sign(binary_str, is_negative, bit_width):
    """
    Pads a binary string and applies two's complement if negative.
    
    @param binary_str - Binary string to process
    @param is negative - whether the original number was negative
    @param bit_width - Desired bit width
    @return - prpcess binary string
    """
    
    padded = binary_str.zfill(bit_width)
    
    if is_negative:
        return twos_complement(padded)
    
    return padded


def invert_bits(binary_str):
    """
    Invert all bits in a binary string (0 becomes 1, 1 becomes 0)
    
    @param binary_str - Binary string to invert
    @return - Inverted binary string of same length
    """
    inverted_bits = []
    
    for bit in binary_str:
        if bit == '0':
            inverted_bits.append('1')
        else:
            inverted_bits.append('0')
    
    return ''.join(inverted_bits)



def mask_to_32bits(value, as_unsigned=True):
    """
    Mask a value to 32 bits.
    
    @param value - Integer value to mask (can be int, str, or hex)
    @param as_unsigned - If True, return unsigned 0-4294967295.
                         If False, return signed -2147483648 to 2147483647
    @return - Masked integer value within 32-bit range
    """
    # Handle different input types
    if isinstance(value, str):
        # Try to convert from binary or hex string
        if value.startswith('0x') or value.startswith('0X'):
            value = int(value, 16)
        elif all(c in '01' for c in value):
            value = int(value, 2)
        else:
            value = int(value)
    
    # Mask to 32 bits (unsigned)
    masked = value & 0xFFFFFFFF
    
    # Convert to signed if requested
    if not as_unsigned and masked >= 0x80000000:
        masked = masked - 0x100000000
    
    return masked


def mask_binary_string(binary_str):
    """
    Mask a binary string to exactly 32 bits.
    
    @param binary_str - Binary string to mask
    @return - 32-bit binary string (truncated or zero-padded as needed)
    """
    # Remove any spaces or prefixes
    clean_str = binary_str.replace(' ', '').replace('0b', '')
    
    # Truncate or pad to 32 bits
    if len(clean_str) > 32:
        # Keep only the lowest 32 bits (rightmost 32 characters)
        clean_str = clean_str[-32:]
    elif len(clean_str) < 32:
        # Pad with leading zeros
        clean_str = clean_str.zfill(32)
    
    return clean_str


def mask_hex_string(hex_str, prefix="0x"):
    """
    Mask a hexadecimal string to 32 bits (8 hex digits).
    
    @param hex_str - Hexadecimal string (with or without 0x prefix)
    @param prefix - Whether to include 0x prefix in output
    @return - 32-bit hex string with exactly 8 hex digits
    """
    # Remove prefix
    clean = hex_str.replace('0x', '').replace('0X', '')
    
    # Convert to int and mask to 32 bits
    value = int(clean, 16) & 0xFFFFFFFF
    
    # Convert back to hex with 8 digits
    hex_result = f"{value:08X}"
    
    if prefix:
        return f"{prefix}{hex_result}"
    return hex_result
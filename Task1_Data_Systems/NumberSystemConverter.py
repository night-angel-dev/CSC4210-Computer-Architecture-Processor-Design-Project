"""
NumberSystemConverter - here will contain much of the logic for section 1 of our task. This includes:

1. A 32-bit signed decimal input parser
2. Decimal → Binary (Two’s Complement) conversion logic
3. Binary → Hexadecimal conversion logic
4. Binary → Decimal conversion logic
5. Overflow detection for out-of-range inputs
6. Saturation logic to prevent wrap-around
7. Configurable output format selection

@author Armando Galvan
@version CSC4210 Computer Architecture Spring 2026

"""
import re
from binary_utils import (
    decimal_to_padded_binary, 
    binary_to_hexadecimal, 
    binary_to_decimal, 
    binary_addition, 
    twos_complement)

class NumberSystemConverter:
    
    
    def __init__(self):
        
        #constants, you have to include self. or else it is just considerd a local variable
        
        
        # These are instance variables
        
        # representable ranges for FR2
        self.MIN_INT32 = -2**31 # = -2147483648
        self.MAX_INT32 = 2**31 - 1 # = 2147483647
        
        # Internal storage for FR3
        self.internal_binary = None
        self.last_input = None
        self.last_output = None

        
        # Overflow/Saturation booleans for FR4 and Fr5
        self.overflow = False
        self.saturated = False
        
        # FR6 Consistent formatting
        self.hex_prefix = "0x"
        
        
    def decimal_to_signed_32bit(self, decimal_str):
        """
        Input Parser
    
        We need to validate whetehr the user has inputted a decimal. i.e ("123", "-45", "0")
        
        @param decimal_str - Decimal string to parse.
        @return - Returns a tuple that includes the value, 
        a boolean on whether its valid and debug statement. 
        """
        # input is none
        if decimal_str is None:
            return None, False, "Input is None"
        
        # Make sure to convert to string incase its int or other type of variable
        # Strip of whitespaces if any
        decimal_str = str(decimal_str).strip()
        
        
        # If decimal_str was empty or contained any spaces decimal_str would be or have nothing
        if not decimal_str:
            return None, False, "Empty Input"
        
        
        # check each character in decimal_str
        
        # Variables that will be helpful in checking each character
        digit_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        start_index = 0
        
        # checking first character
        
        # check if negative number
        if decimal_str[0] == '-':
            
            # check if theres anything else after, if not its just the negative sign
            if len(decimal_str) == 1:
                return None, False, "Just a minus sign, nothing else."
            
            # start from second element
            start_index = 1
        elif decimal_str[0] in digit_characters:
            # No need to do anything
            pass
        
        else:
            # if we are, we know the character is invalid
            return None, False, f"Invalid first character '{decimal_str[0]}' "
        

        # Now we can loop through the rest of the string with no problem
        for i in range(start_index, len(decimal_str)):
            
            # check if each characters is not a digit, if not return 
            if decimal_str[i] not in digit_characters:
                return None, False, f"Invalid chracter ('{decimal_str[i]}') at position {i}"
            
        # If we are here, then everything has gone smooth
        value = int(decimal_str)
        
        return value, True, ""
    

    def decimal_to_padded_binary(self, value, bit_width = 32):
        """
        Converts a decimal integer value into a binary value. 
        
        @param value - decimal integer value 
        @param bit_width - number of bits (default 32)
        @return - Returns binary equivalent value to decimal integer value
        """
    
        return decimal_to_padded_binary(value, 32)
        
    
    
    def twos_complement(self, binary_str):
        """
        Converts a binary to its negative version using twos complement logic
        
        @param binary_str - binary being converted to negative version
        @return - negative version of positive binary
        """
        
        return twos_complement(binary_str)
    
    
    def binary_addition(self, binary_str1, binary_str2):
        """
        Add two binary strings using bit by bit addition with carry.

        @param binary_str1 - First binary string
        @param binary_str2 - Second binary string
        @return - Sum as binary string
        """
        
        return binary_addition(binary_str1, binary_str2)
 
    
    def binary_to_hexadecimal(self, value):
        """
        Converts a binary value to a hexadecimal value.
        
        @param value - binary value being converted to hexadecimal value
        @return - the hexadecimal value 
        """
        
        return binary_to_hexadecimal(value, self.hex_prefix)
        
    
    
    
    def binary_to_decimal(self, value):
        """
        Converts a 32 bit binary value to decimal value
        
        @param value - Binary value being converted to decimal
        @return - Binary's decimal value
        """    
        
        return binary_to_decimal(value)
    
    
    
    def detect_overflow(self, value):
        """
        Detects if value is outside 32 bit signed range
        
        @param value - decimal value 
        @return - Boolean on whether value is outisde 32 bit signed range
        
        """
        return value < self.MIN_INT32 or value > self.MAX_INT32
    
    
    
    def apply_saturation(self, value):
        """
        This method applys saturation (clamping) , not wrap around, in the case of overflow
        
        @param value - 32 bit signed value
        @return - value with saturation applied
        
        """
        
        if value > self.MAX_INT32:
            self.saturated = True
            return self.MAX_INT32
        
        elif value < self.MIN_INT32:
            self.saturated = True
            return self.MIN_INT32
        
        else:
            self.saturated = False
            return value
        
    
    def format_output(self, value, format_type):
        """
        Reformat a value in one of the following formats (Binary, Hexadecimal, Decimal)
        
        @param value - value being reformatted
        @param format_type - format type being requested ("DEC", "BIN", "HEX")
        @return - value in request format
        
        """
        #standardize input
        format_type = format_type.upper()
        
        # We should create a method just for identify the type of input
        # Here however we will assume that the input is already in decimal format
        
        if format_type == "DEC":
            return str(value)
        
        elif format_type == "BIN":
            return self.decimal_to_padded_binary(value)
        
        elif format_type == "HEX":
            
            # covnert to binary then to hex
            binary = self.decimal_to_padded_binary(value)
            return self.binary_to_hexadecimal(binary)
        
        else:
            raise ValueError(f"Input is in invalid format: {format_type}")
        

    def convert(self, decimal_str, output_format):
        """
        This is the main conversion method that implements all other conversion methods.
        
        @param decimal_str - decimal string being converted to a specific format
        @param output_format - the format specified
        @return - the value converted to specified format
        
        """
        # Parse input
        value, is_valid, error = self.decimal_to_signed_32bit(decimal_str)
        
        if not is_valid:
            return f"Debug error: {error}", 0 , 0
        
        self.last_input = value 
        
        
        # detect is value is out of limits of 32 bit signed integer value range
        self.overflow = self.detect_overflow(value)
        
        # Apply saturation if needed
        clamped_value = self.apply_saturation(value)
        
        
        # store internal 32 bit binary represnetation 
        self.internal_binary = self.decimal_to_padded_binary(clamped_value)
        self.last_output = clamped_value
        
        
        # format output as requestion
        formatted = self.format_output(clamped_value, output_format)
        
        
        # return with flags as ints
        overflow_int = 1 if self.overflow else 0
        saturated_int = 1 if self.saturated else 0
        
        return formatted, overflow_int, saturated_int
        
        

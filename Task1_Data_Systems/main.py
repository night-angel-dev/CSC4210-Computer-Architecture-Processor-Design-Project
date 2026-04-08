"""
main.py - Main interface for Task 1 Data Systems

@author Armando Galvan
@version CSC4210 Computer Architecture Spring 2026

"""


from NumberSystemConverter import NumberSystemConverter

def main():
    
    converter = NumberSystemConverter()
    
    
    print("\n" + "="*60)
    print("32-BIT SIGNED INTEGER CONVERTER")
    print("="*60)
    print("Converts decimal to DEC/BIN/HEX with overflow detection")
    print("-" * 60)


    while True:
        
            
        # get Input 
        print("\n Enter a decminal integer (or 'q' to exit program): ")
        
        decimal_str = input("").strip().upper()
        
        if decimal_str.lower() == 'q':
            print("Exiting Program")
            break
        
        if not decimal_str:
            print("Please enter a value")
            
        
        # Get the format
        print("\nOutput format? Enter from the following (DEC, BIN, HEX) ")
        format = input("").strip().upper()
        
        if format not in ['DEC', 'BIN', 'HEX']:
            print("Invalid format. Enter DEC, BIN, or HEX ")
            continue
        
        # convert and display
        result, overflow, staturated = converter.convert(decimal_str, format)
        
        
        print("\n" + "-" * 40 )
        print(f"Result: {result}")
        print(f"Overflow: {overflow}  |  Saturated: {staturated}")
        print("-" * 40)
                    
            


if __name__ == "__main__":
    main()
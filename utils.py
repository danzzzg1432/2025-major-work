def format_large_number(num):  
    """
    The game has numbers in the vigintillions - aka 20 zeros. Trying to display that on the screen is a bit too much,
    so this is a function that summarises the number.
    """
    if num < 1000:
        return str(int(num)) # if the number is less than 1000, return it as an integer as no change is needed
    
    magnitude = 0 # initialise the magnitude of the number
    while abs(num) >= 1000: 
        magnitude += 1 
        num /= 1000.0 # divide by 1000 to get the next major magnitude (thousands, millions, billions, etc.)
    
    # Format with 3 decimal places and remove trailing zeros
    formatted_num = f"{num:.3f}".rstrip('0').rstrip('.')
    
    # Return formatted number with appropriate suffix
    suffixes = ["", "K", "MILLION", "BILLION", "TRILLION", "QUADRILLION", 
                "QUINTILLION", "SEXTILLION", "SEPTILLION", "OCTILLION", "NONILLION", "DECILLION", "UNDECILLION", 
                "DUODECILLION", "TREDECILLION", "QUATTUORDECILLION", "QUINDECILLION", "SEXDECILLION", "SEPTENDECILLION", 
                "OCTODECILLION", "NOVEMDECILLION", "VIGINTILLION"]
    
    if magnitude < len(suffixes):
        return f"{formatted_num} {suffixes[magnitude]}" # if the number has a pretty suffix, return it with the suffix
    else:
        return f"{formatted_num}e{magnitude*3}" # if the number is too large, return it in scientific notation

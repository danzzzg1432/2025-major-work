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
    suffixes = [
            "",    "K",   "M",   "B",   "T",    "Qa",   "Qi",   "Sx",   "Sp",   "Oc",   # 10^0…10^27
            "No",  "Dc",  "Ud",  "Dd",  "Td",   "Qad",  "Qid",  "Sxd",  "Spd",  "Ocd",  # 10^30…10^57
            "Nod", "Vg",  "Vd",  "Tg",  "Qag",  "Qig",  "Sxg",  "Spg",  "Uvg",  "Dvg",  # 10^60…10^87
            "Tvg", "Qavg","Qivg","Sxvg","Spvg"                                            # 10^90…10^102
           ]
    
    if magnitude < len(suffixes):
        return f"{formatted_num} {suffixes[magnitude]}" # if the number has a pretty suffix, return it with the suffix
    else:
        return f"{formatted_num}e{magnitude*3}" # if the number is too large, return it in scientific notation







def verify_string(string, min_len, max_len):
    if type(string) != str:
        return False, f'Variable Expected Was str | Recieved: {type(string)} | Data: {string}'
    
    if len(string) < min_len:
        return False, f'Minimum String Len Expected: {min_len} | Recieved: {len(string)} | Data: {string}'
    
    if len(string) > max_len:
        return False, f'Maximum String Len Expected: {max_len} | Recieved: {len(string)} | Data: {string}'
    
    return True, ""

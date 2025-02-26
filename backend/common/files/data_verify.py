def verify_string(string, min_len, max_len):
    if type(string) is not str:
        return False, f'Variable Expected Was str | Recieved: {type(string)} | Data: {string}'
    
    if len(string) < min_len:
        return False, f'Minimum String Len Expected: {min_len} | Recieved: {len(string)} | Data: {string}'
    
    if len(string) > max_len:
        return False, f'Maximum String Len Expected: {max_len} | Recieved: {len(string)} | Data: {string}'
    
    return True, ""


def verify_integer(integer, min, max):
    if type(integer) is not int:
        return False, f'Variable Expected Was int | Recieved: {type(integer)} | Data: {integer}'
    
    if integer < min:
        return False, f'Minimum Number Expected: {min} | Data: {integer}'
    
    if integer > max:
        return False, f'Maximum Number Expected: {max} | Data: {integer}'
    
    return True, ""


def verify_boolean(boolean):
    if type(boolean) is not bool:
        return False, f'Variable Expected Was bool | Recieved: {type(boolean)} | Data: {boolean}'
    
    return True, ""


def verify_list(lst, min_len, max_len):
    if type(lst) is not list:
        return False, f'Variable Expected Was list | Recieved: {type(lst)} | Data: {lst}'
    
    if len(lst) < min_len:
        return False, f'Minimum Values Len Expected: {min_len} | Recieved: {len(lst)} | Data: {lst}'
    
    if len(lst) > max_len:
        return False, f'Maximum Values Len Expected: {max_len} | Recieved: {len(lst)} | Data: {lst}'
    
    return True, ""














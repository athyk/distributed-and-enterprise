def verify_string(string: any, min_len: int, max_len: int) -> tuple[bool, str]:
    """
    This function checks to see if the given variable is a string within the specified length range
    """

    s_len = len(string)
    s_type = type(string)

    if s_type is not str:
        return False, f'Variable Expected Was str | Received: {s_type} | Data: {string}'
    
    if s_len < min_len:
        return False, f'Minimum String Len Expected: {min_len} | Received: {s_len} | Data: {string}'
    
    if s_len > max_len:
        return False, f'Maximum String Len Expected: {max_len} | Received: {s_len} | Data: {string}'
    
    return True, ""


def verify_integer(integer: any, min: int, max: int) -> tuple[bool, str]:
    """
    This function checks to see if the given variable is an integer within the specified range
    """

    i_type = type(integer)

    if i_type is not int:
        return False, f'Variable Expected Was int | Received: {i_type} | Data: {integer}'
    
    if integer < min:
        return False, f'Minimum Number Expected: {min} | Data: {integer}'
    
    if integer > max:
        return False, f'Maximum Number Expected: {max} | Data: {integer}'
    
    return True, ""


def verify_boolean(boolean: any) -> tuple[bool, str]:
    """
    This function checks to see if the given variable is a boolean
    """

    b_type = type(boolean)

    if b_type is not bool:
        return False, f'Variable Expected Was bool | Received: {b_type} | Data: {boolean}'
    
    return True, ""


def verify_list(lst: any, min_len: int, max_len: int) -> tuple[bool, str]:
    """
    This function checks to see if the given variable is a list within the specified length range
    """

    l_len = len(lst)
    lst_type = type(lst)

    if lst_type is not list:
        return False, f'Variable Expected Was list | Received: {lst_type} | Data: {lst}'
    
    if l_len < min_len:
        return False, f'Minimum Values Len Expected: {min_len} | Received: {l_len} | Data: {lst}'
    
    if l_len > max_len:
        return False, f'Maximum Values Len Expected: {max_len} | Received: {l_len} | Data: {lst}'
    
    return True, ""

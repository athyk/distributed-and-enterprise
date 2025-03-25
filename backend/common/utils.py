def verify_string(string: any, min_len: int, max_len: int, var_name: str = 'No Var') -> tuple[bool, str]:
    """
    This function checks to see if the given variable is a string within the specified length range
    """

    s_len = len(string)
    s_type = type(string)

    if s_type is not str:
        return False, f'Expected {var_name} To Be A str | Received: {s_type} | Data: {string}'
    
    if s_len < min_len:
        return False, f'{var_name} | Minimum String Len Expected: {min_len} | Received: {s_len} | Data: {string}'
    
    if s_len > max_len:
        return False, f'{var_name} | Maximum String Len Expected: {max_len} | Received: {s_len} | Data: {string}'
    
    return True, ""


def verify_integer(integer: any, min: int, max: int, var_name: str = 'No Var') -> tuple[bool, str]:
    """
    This function checks to see if the given variable is an integer within the specified range
    """

    i_type = type(integer)

    if i_type is not int:
        return False, f'Expected {var_name} To Be A int | Received: {i_type} | Data: {integer}'
    
    if integer < min:
        return False, f'{var_name} | Minimum Number Expected: {min} | Data: {integer}'
    
    if integer > max:
        return False, f'{var_name} | Maximum Number Expected: {max} | Data: {integer}'
    
    return True, ""


def verify_boolean(boolean: any, var_name: str = 'No Var') -> tuple[bool, str]:
    """
    This function checks to see if the given variable is a boolean
    """

    b_type = type(boolean)

    if b_type is not bool:
        return False, f'Expected {var_name} To Be A bool | Received: {b_type} | Data: {boolean}'
    
    return True, ""


def verify_list(lst: any, min_len: int, max_len: int, var_name: str = 'No Var') -> tuple[bool, str]:
    """
    This function checks to see if the given variable is a list within the specified length range
    """

    l_len = len(lst)
    lst_type = type(lst)

    if lst_type is not list:
        return False, f'Expected {var_name} To Be A list | Received: {lst_type} | Data: {lst}'
    
    if l_len < min_len:
        return False, f'{var_name} | Minimum Values Len Expected: {min_len} | Received: {l_len} | Data: {lst}'
    
    if l_len > max_len:
        return False, f'{var_name} | Maximum Values Len Expected: {max_len} | Received: {l_len} | Data: {lst}'
    
    return True, ""


def is_password_valid(val: str):
    """Returns True if password meets the following criteria:
     
    - between 8 and 20 characters in length.
    - at least 1 upper case char 
    - at least 1 lower case char
    - at least 1 number"""
    try:
        if len(val) >= 8 and len(val) <= 20:
            if any(s.isupper() for s in val):
                if any(s.islower() for s in val):
                    if any(s.isdigit() for s in val):
                        return True
        return False
    except:
        return False


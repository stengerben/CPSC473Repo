# cookies.py
import hashlib
import hmac

SECRET = 's00p3rs33kr1t'
DELIMITER = '|'

def _hash(s):
    """
    Returns the SHA-256 HMAC of s using key SECRET
    """
    return hmac.new(SECRET, str(s), hashlib.sha256).hexdigest()

def _sign(s):
    """
    Returns s, signed

    Example:

        _sign('bar')

    will return 'bar|b50e06b7a3c2b6103e0526fe5ad871ad18d5b2edd1dc63e2d7ba96bd985c1384'
    if DELIMITER is '|'
    """
    return s+'|'+_hash(s)

def _value(cookie):
    """
    Returns the value of a signed cookie

    Example:

        _value('bar|b50e06b7a3c2b6103e0526fe5ad871ad18d5b2edd1dc63e2d7ba96bd985c1384')

    will return 'bar' if DELIMITER is '|' and the signature is valid,
    and None otherwise.
    """
    value = cookie.split('|')
    if (_hash(value[0]) == value[1]):
        return value[0]
    else:
        return None

def get(request, variable, default=None):
    """
    Returns the value of the signed variable, or default if
       (1) The variable was not included in the request
       (2) The variable was tampered with

    Example:
        
        get(request, 'foo', 'baz')

    will return 'bar' for the following header:

        Cookie: foo=bar|b50e06b7a3c2b6103e0526fe5ad871ad18d5b2edd1dc63e2d7ba96bd985c1384

    and 'baz' otherwise
    """
    if request.cookies.get(variable):
        value = request.cookies.get(variable).split('|')
        if (_hash(value[0]) == value[1]):
            return value[0]
        else:
            return default
    else:
        return default
    
def set(response, variable, value):
    """
    Adds a signed Set-Cookie header to response for variable=value

    Example:

        set(response, 'foo', 'bar')

    adds the following header:

        Set-Cookie: foo=bar|b50e06b7a3c2b6103e0526fe5ad871ad18d5b2edd1dc63e2d7ba96bd985c1384
    """
    cookieVal = str(value)+'|'+_hash(str(value))
    response.set_cookie(variable, cookieVal)

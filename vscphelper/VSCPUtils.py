

def checkRangeOfInt(var, name, _min=0, _max=255):
     if not isinstance(var, int):
            raise TypeError("{0} must be a integer".format(name))
     elif var<_min or var>_max:
         raise ValueError("{0} is out of range [{1},{2}]".format(name, str(_min), str(_max)))
     else:
         return True
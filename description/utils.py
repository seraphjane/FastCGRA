def list2str(lst): 
    assert isinstance(lst, list) or isinstance(lst, tuple)
    result = "(List: ["
    for elem in lst: 
        if isinstance(elem, list) or isinstance(elem, tuple): 
            elem = list2str(elem)
        elif isinstance(elem, dict): 
            elem = dict2str(elem)
        result += elem + ", "
        if len(result) > 64: 
            result += "\n "
    result += "])"
    return result

def dict2str(dct): 
    assert isinstance(dct, dict)
    result = "(Dict: {\n"
    for key in dct: 
        elem = str(dct[key])
        if isinstance(elem, list) or isinstance(elem, tuple): 
            elem = list2str(elem)
        elif isinstance(elem, dict): 
            elem = dict2str(elem)
        result += "\t -- " + key + ": \t" + elem + "\n"
    result += "})"
    return result

class Base: 
    def info(self): 
        return "UNKNOWN"
PRESERVED_ATTRIBUTES = {
    'name', 'value', 'type', 'data', 'id', 'key',
    'items', 'keys', 'values', 'count', 'index',
    'size', 'length', 'result', 'error',
    
    'append', 'extend', 'insert', 'remove', 'pop',
    'clear', 'sort', 'reverse', 'copy', 'update',
    'get', 'set', 'add', 'delete',
    
    'category', 'categories',           
    'stock',          
    'price',
    'product_id',
    'quantity',          
    
    'str', 'int', 'float', 'bool', 'list', 'dict',
    'set', 'tuple', 'bytes', 'type', 'object',
    
    'self', 'cls', 'args', 'kwargs',
    'None', 'True', 'False',
    
    '__init__', '__str__', '__repr__', '__len__',
    '__getitem__', '__setitem__', '__delitem__',
    '__iter__', '__next__', '__call__', '__enter__',
    '__exit__', '__get__', '__set__', '__delete__',
    '__add__', '__sub__', '__mul__', '__div__',
    '__mod__', '__eq__', '__ne__', '__lt__', '__gt__',
    '__le__', '__ge__'
}

OBFUSCATE_PARAMS = {
    'product', 'products',
    'total', 'amount',
    'description', 'details', 'status', 'state'
}

def should_preserve(name: str, is_param: bool = False) -> bool:
    if is_param and name in OBFUSCATE_PARAMS:
        return False
        
    return (name in PRESERVED_ATTRIBUTES or
            name.startswith('__') or      
            name.startswith('_abc_'))       
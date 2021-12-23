import struct

class F_INT:
    pass

class F_FLOAT:
    pass

class F_STRING:
    pass

class F_Type_Utils:
    type_to_num_folders = {
        F_INT: 0,
        F_FLOAT: 1,
        F_STRING: 2,
    }
    
    type_map = {
        int: F_INT,
        float: F_FLOAT,
        str: F_STRING,
    }

    reverse_type_map = {
        F_INT: int,
        F_FLOAT: float,
        F_STRING: str,
    }

    @staticmethod
    def ptype_to_ftype(ptype):
        return F_Type_Utils.type_map[ptype]

    @staticmethod
    def ftype_to_ptype(ftype):
        return F_Type_Utils.reverse_type_map[ftype]

    #https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
    @staticmethod
    def float_binary(num):
        return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))
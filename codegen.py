from functools import reduce

class CodeGen:
    def gen_class_code(self, layer_name, fields):
        codes = [
            self.gen_class_base_code(layer_name),
            self.gen_fields_code(fields),
            self.gen_init_code()
        ]
        return reduce(lambda x, y: x + y, codes)

    def gen_class_base_code(self, layer_name):
        class_base_code = f"""import random

from layers.layer import Layer
from scapy.all import {layer_name}

class {layer_name}Layer:
    name = "{layer_name}"
    protocol = {layer_name}

"""
        return class_base_code
        
    def gen_fields_code(self, fields):
        fields_lines = [f"        '{field}'," for field in fields]
        fields_lines_combined = reduce(lambda x, y: x + '\n' + y, fields_lines)
        fields_code = f"""    _fields = [
{fields_lines_combined}
    ]
    fields = _fields
"""
        return fields_code

    def gen_init_code(self):
        init_code = f"""
    def __init__(self, layer):
        Layer.__init__(self, layer)
        # Special methods to help access fields that cannot be accessed normally
        # self.getters = {{}} # TODO
        # self.setters = {{}}
        # Special methods to help access fields that cannot be generated normally
        # self.generators = {{}} # TODO
"""
        return init_code


if __name__ == '__main__':
    codegen = CodeGen()
    # print(codegen.gen_fields_code(['abc', 'def']))
    print(codegen.gen_class_code('IP', ['abc', 'def', 'ghi']))

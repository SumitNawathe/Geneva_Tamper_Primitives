from functools import reduce

class CodeGen:
    def gen_class_code(self, layer_name, fields):
        field_names = self.fields_to_field_names(fields)
        codes = [
            self.gen_class_base_code(layer_name),
            self.gen_fields_code(field_names),
            self.gen_init_code(),
            self.gen_all_gens_code(fields)
        ]
        return self.combine_codes(codes, newline=False)

    def gen_class_base_code(self, layer_name):
        class_base_code = f"""import random

from layers.layer import Layer
from scapy.all import {layer_name}

class {layer_name}Layer(Layer):
    name = "{layer_name}"
    protocol = {layer_name}

"""
        return class_base_code
        
    def gen_fields_code(self, field_names):
        fields_lines = [f"        '{field_name}'," for field_name in field_names]
        fields_lines_combined = self.combine_codes(fields_lines, newline=True)
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

    def gen_gen_code(self, field_name, field_len):
        max_val = 2 ** field_len - 1
        gen_code = f"""
    def gen_{field_name}(self, field):
        return random.randint(1, {max_val})
"""
        return gen_code

    def gen_all_gens_code(self, fields):
        gen_codes = [self.gen_gen_code(field_name, field_len) for field_name, field_len in fields]
        return self.combine_codes(gen_codes, newline=False)

    def fields_to_field_names(self, fields):
        return [field[0] for field in fields]

    def combine_codes(self, codes, newline=False):
        newline_char = '\n' if newline else ''
        return reduce(lambda x, y: x + newline_char + y, codes)

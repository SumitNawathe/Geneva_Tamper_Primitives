import io
from parse_diagram import *
from codegen import CodeGen

header = io.open("udp_header.txt").read()
fields = parse_diagram(header)
cleaned_fields = collect_options(fields)
final_fields = make_abbr(cleaned_fields)
codegen = CodeGen()
print(codegen.gen_class_code('UDP', final_fields))

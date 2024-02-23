import base64
content = "ZnJvbSBkamFuZ28uYXBwcyBpbXBvcnQgQXBwQ29uZmlnCgoKY2xhc3MgQXBp\nQ29uZmlnKEFwcENvbmZpZyk6CiAgICBkZWZhdWx0X2F1dG9fZmllbGQgPSAi\nZGphbmdvLmRiLm1vZGVscy5CaWdBdXRvRmllbGQiCiAgICBuYW1lID0gImFw\naSIK\n"


data = base64.b64decode(content)

import ast
import astor

# def clean_and_format_python_code(data):
#     # Decode the data if it's in bytes format
#     if isinstance(data, bytes):
#         data = data.decode('utf-8')

#     # Parse the Python code
#     parsed_ast = ast.parse(data)

#     # Pretty-print the AST to a string
#     formatted_code = astor.to_source(parsed_ast)

#     return formatted_code

# Example usage
# data = b'from django.apps import AppConfig\n\n\nclass ApiConfig(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "api"\n'
# cleaned_and_formatted_code = clean_and_format_python_code(data)
# print(cleaned_and_formatted_code)

print(data)
data = data.decode('utf-8')
print(data)

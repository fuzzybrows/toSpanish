import os

files = [file.rstrip(".py") for file in
         os.listdir(os.path.dirname(__file__)) if file.endswith(".py") and '__init__' not in file]
for file in files:
    exec(f"from .{file} import *")
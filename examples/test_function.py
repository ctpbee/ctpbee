import types


d = types.ModuleType("object")
with open("func.py", "rb") as f:
    d.__file__ = f.name
    exec(compile(f.read(), f.name, 'exec'), d.__dict__)


print(type(d.ext))
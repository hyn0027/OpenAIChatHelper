from . import StringOperations

for name in dir(StringOperations):
    if not name.startswith("__"):
        globals()[name] = getattr(StringOperations, name)
